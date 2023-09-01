import os
from django.shortcuts import get_object_or_404
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.files.storage import default_storage
from django.http import HttpResponse, Http404
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.db import transaction
from django.db.models import Q
from datetime import datetime
import qrcode
import base64
import io

from django.views.generic import ListView, DetailView, CreateView, UpdateView
from accounts.mixins import FieldsMixin, FormValidMixin, AuthAccInsrtInsMixin
from .forms import InstructionForm, InsChangeForm
from .models import Instruction, Attachment
from django.views import View


class InstructionRestoreView(View):
    def get(self, request, instruction_id):
        instruction = get_object_or_404(Instruction, id=instruction_id)
        instruction.is_active = True
        instruction.save()
        return redirect('self_instruction_list')


def increase_download(request, attachment_id):
    attachment = get_object_or_404(Attachment, id=attachment_id)
    attachment.increase_download_count()

    response = {
        'download_count': attachment.download_count,
        'file_url': attachment.file.url
    }
    # print('download_count')

    return JsonResponse(response)


class InsDetailView(DetailView):
    model = Instruction
    template_name = 'instructions/ins_detail.html'
    context_object_name = 'instruction'

    def get_queryset(self):
        return super().get_queryset().prefetch_related('instruction_attach')

    # def increase_download(self, request, attachment_id):
    #     attachment = Attachment.objects.get(id=attachment_id)
    #     attachment.increase_download_count()
    #     return redirect(attachment.file.url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instruction = self.get_object()

        # Create QR code for each uploaded file
        attachments = instruction.instruction_attach.all()
        qr_codes = []
        attachment_download_counts = []

        for attachment in attachments:
            if attachment.file and default_storage.exists(attachment.file.name):
                file_url = self.request.build_absolute_uri(attachment.file.url)
                qr = qrcode.QRCode(version=1, box_size=3, border=3)
                qr.add_data(file_url)
                qr.make(fit=True)
                img = qr.make_image(fill_color="black", back_color="white")
                img_buffer = io.BytesIO()
                img.save(img_buffer, format='PNG')
                img_data = base64.b64encode(img_buffer.getvalue())
                qr_codes.append(img_data.decode('utf-8'))

                attachment_download_counts.append(attachment.download_count)

        context['qr_codes'] = qr_codes
        context['attachments'] = attachments
        context['attachment_download_counts'] = attachment_download_counts

        return context


def ins_delete(request, pk):
    instruction = get_object_or_404(Instruction, id=pk)
    if request.method == 'POST':
        instruction.is_active = False
        instruction.save()
        return redirect('instruction_list')
    return render(request, 'instructions/ins_delete.html', {'instruction': instruction})


class InsUpdateView(LoginRequiredMixin, UpdateView):
    model = Instruction
    form_class = InsChangeForm
    template_name = 'instructions/ins_update.html'
    success_url = reverse_lazy('self_instruction_list')

    # context_object_name = 'instruction'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        instruction = self.get_object()
        context['attachments'] = instruction.instruction_attach.all()
        return context

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.user = self.object.user
            if not form.cleaned_data['for_behvarz'] and not form.cleaned_data['for_expert']:
                messages.error(
                    self.request, 'حداقل یکی از موارد بهورز یا کارشناس را انتخاب کنید.')
                return super().form_invalid(form)

            # Save the form
            instance = form.save(commit=False)

            # Delete selected attachments
            attachments = self.request.POST.getlist('delete-checkbox')
            print("Selected attachments:", attachments)
            print("Instance:", instance)
            attachments_to_delete = Attachment.objects.filter(id__in=attachments, ins_attach=instance)
            print("Attachments to delete:", attachments_to_delete)
            for attachment in attachments_to_delete:
                # Delete the file from storage
                file_path = attachment.file.path
                print("File path:", file_path)
                default_storage.delete(file_path)
                # Delete the attachment
                attachment.delete()

            instance.save()

        messages.success(self.request, 'محتوا با موفقیت ارسال شد.')
        return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request, f'خطا در فیلد {form.fields[field].label}: {error}')
        return self.render_to_response(self.get_context_data(form=form, ))

    # def form_invalid(self, form):
    #     # اضافه کردن خطاها به فرم
    #     for field in form.errors:
    #         for error in form.errors[field]:
    #             form.add_error(field, error)

    #     # بازگرداندن فرم به تمپلیت
    #     return self.render_to_response(self.get_context_data(form=form))

    # def form_valid(self, form):
    #     instruction = form.save(commit=False)
    #     instruction.user = self.request.user

    #     # چاپ مقادیر فیلدهای مدل Instruction
    #     print(instruction.type)
    #     print(instruction.status)

    #     instruction.save()
    #     form.save_m2m()

    #     attachments = self.request.FILES.getlist('attachments')
    #     for attachment in attachments:
    #         attachment_instance = Attachment.objects.create(
    #             ins_attach=instruction,
    #             file=attachment,
    #             file_name=os.path.basename(attachment.name),
    #             file_size=attachment.size,
    #         )
    #         instruction.instruction_attach.add(attachment_instance)

    #     return super().form_valid(form)


class InsCreateView(LoginRequiredMixin, FieldsMixin, FormValidMixin, CreateView):
    model = Instruction
    template_name = 'instructions/ins_create.html'
    success_url = reverse_lazy('self_instruction_list')

    def form_valid(self, form):
        with transaction.atomic():
            form.instance.user = self.request.user
            if not form.cleaned_data['for_behvarz'] and not form.cleaned_data['for_expert']:
                messages.error(
                    self.request, 'حداقل یکی از موارد بهورز یا کارشناس را انتخاب کنید.')
                return super().form_invalid(form)
            form.save()

            attachments = self.request.FILES.getlist('attachment')
            for attachment in attachments:
                Attachment.objects.create(
                    ins_attach=form.instance, file=attachment)

            messages.success(self.request, 'محتوا با موفقیت ارسال شد.')
            return super().form_valid(form)

    def form_invalid(self, form):
        for field, errors in form.errors.items():
            for error in errors:
                messages.error(
                    self.request, f'خطا در فیلد {form.fields[field].label}: {error}')
        return self.render_to_response(self.get_context_data(form=form))


class SelfInsListView(LoginRequiredMixin, ListView):
    model = Instruction
    template_name = 'instructions/self_ins_list.html'
    context_object_name = 'instructions'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
            return Instruction.objects.filter(user_id=user_id).order_by('-datetime_created')
        return Instruction.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['last_visited'] = self.request.session.get('last_visited')
        self.request.session['last_visited'] = timezone.now().isoformat()

        return context

    @property
    def download_counts(self):
        if not hasattr(self, '_download_counts'):
            self._download_counts = {
                instruction.id: instruction.download_count for instruction in self.object_list}
        return self._download_counts


class InsListView(LoginRequiredMixin, ListView):
    model = Instruction
    template_name = 'instructions/ins_list.html'
    context_object_name = 'instructions'

    def get_queryset(self):
        queryset = super().get_queryset()

        # Apply search filters
        search_query = self.request.GET.get('q')
        type_filter = self.request.GET.get('type')
        start_date_filter = self.request.GET.get('start_date')
        end_date_filter = self.request.GET.get('end_date')
        status_filter = self.request.GET.get('status')

        if search_query:
            queryset = queryset.filter(Q(title__icontains=search_query) | Q(
                description__icontains=search_query))

        if type_filter:
            queryset = queryset.filter(type=type_filter)

        if start_date_filter:
            queryset = queryset.filter(datetime_created__gte=start_date_filter)

        if end_date_filter:
            queryset = queryset.filter(datetime_created__lte=end_date_filter)

        if status_filter:
            queryset = queryset.filter(status=status_filter)

        # Prefetch related instruction_attach and calculate download counts
        queryset = queryset.prefetch_related('instruction_attach')
        download_counts = {instruction.id: instruction.instruction_attach.count()
                           for instruction in queryset}

        # Add download_counts to context
        self.download_counts = download_counts

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Add download_counts to context
        context['download_counts'] = self.download_counts

        # Add type_choices to context
        form = InstructionForm()
        context['type_choices'] = form.fields['type'].choices

        return context


class InstructionDownloadView(View):
    def get(self, request, instruction_id):
        instruction = get_object_or_404(Instruction, id=instruction_id)

        # Increment the download count for the instruction
        instruction.increment_download_count()

        # Get the attachment related to the instruction (assuming only one attachment per instruction)
        attachment = instruction.instruction_attach.first()

        if attachment:
            # Generate the response with the file
            file_path = attachment.file.path
            with open(file_path, 'rb') as file:
                response = HttpResponse(
                    file.read(), content_type='application/octet-stream')
                response['Content-Disposition'] = f'attachment; filename="{attachment.file_name}"'
                return response
        else:
            return HttpResponse("فایل ضمیمه وجود ندارد.")


class InsListViewDeleted(ListView):
    model = Instruction
    template_name = 'instructions/ins_list_deleted.html'
    context_object_name = 'instructions'

    def get_queryset(self):
        return Instruction.objects.filter(is_active=False)
