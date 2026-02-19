from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView , CreateView , DetailView , ListView
# Create your views here.
from .models import Trip , Note
class HomeView(TemplateView):
    template_name = 'trip/index.html'
    
def trips_list(request):
    trips = Trip.objects.filter(owner = request.user)
    context = {
        'trips' : trips
    }
    
    return render(request,'trip/trip_list.html', context)


class TripCreateView(CreateView):
    model = Trip
    success_url = reverse_lazy('trip-list')
    fields = ['city', 'country', 'start_date', 'end_date']
    # template named model_form.html
    
    def form_valid(self, form):
        # owner field = logged in user
        form.instance.owner = self.request.user
        return super().form_valid(form)
    
class TripDetailView(DetailView):
    model = Trip
    
    # data stored on trip - also have the Notes data
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        trip = context['object']
        notes = trip.notes.all()
        context['notes'] = notes
        return context
    
class NoteDetailView(DetailView):
    model = Note
    
    
class NoteListView(ListView):
    model = Note
    
    def get_queryset(self):
        queryset = Note.object.filter(trip_owner = self.request.user)
        return queryset
    