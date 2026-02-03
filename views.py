class AddReviewView(CreateView):
    model = Review
    form_class = ReviewForm
    template_name = 'reviews/add_review.html'
    success_url = reverse_lazy('admin')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получаем врача по ID из URL или другим способом
        # Пример: если ID врача передается в URL как pk
        from .models import Doctor
        doctor_id = self.kwargs.get('pk')
        doctor = Doctor.objects.get(id=doctor_id)
        
        context['doctor'] = doctor
        # Если есть поле specialties (предположим, что это ManyToManyField)
        specialties = doctor.specialties.all()
        context['specialties_text'] = ', '.join([spec.name for spec in specialties])
        return context

    def form_valid(self, form):
        # Установите врача для отзыва перед сохранением
        doctor_id = self.kwargs.get('pk')
        from .models import Doctor
        doctor = Doctor.objects.get(id=doctor_id)
        form.instance.doctor = doctor
        
        # Установите IP-адрес пользователя
        form.instance.ip_address = self.request.META.get('REMOTE_ADDR')
        
        # Если пользователь авторизован, установите его
        if self.request.user.is_authenticated:
            form.instance.user = self.request.user
        else:
            form.instance.is_anonymous = True
        
        messages.success(self.request, message='Отзыв успешно отправлен!')
        return super().form_valid(form)
