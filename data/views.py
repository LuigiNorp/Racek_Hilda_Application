from django.shortcuts import render, redirect
from .forms import CSVUploadForm
from .resources import (
    ClienteResource,
    SedeResource,
    DocumentosClienteResource,
    CarpetaClienteGeneralesResource,
    CarpetaClientePagosResource,
    CarpetaClienteContactosResource,
    PaqueteCapacitacionResource,
    RepresentanteTrabajadoresResource
)
from tablib import Dataset


def import_data(request):
    if request.method == "POST":
        csv_file = request.FILES["csv_file"]
        data_set = csv_file.read().decode('UTF-8').splitlines()
        resources = {
            'Cliente': ClienteResource,
            'Sede': SedeResource,
            'DocumentosCliente': DocumentosClienteResource,
            'CarpetaClienteGenerales': CarpetaClienteGeneralesResource,
            'CarpetaClientePagos': CarpetaClientePagosResource,
            'CarpetaClienteContactos': CarpetaClienteContactosResource,
            'PaqueteCapacitacion': PaqueteCapacitacionResource,
            'RepresentanteTrabajadores': RepresentanteTrabajadoresResource,
        }
        current_resource = None
        dataset = Dataset()
        for line in data_set:
            if line in resources:
                # If we've reached a new section, import the previous section's data
                if current_resource:
                    result = current_resource().import_data(dataset, dry_run=True)
                    if not result.has_errors():
                        current_resource().import_data(dataset, dry_run=False)
                # Start a new section
                current_resource = resources[line]
                dataset.headers = next(data_set)
            else:
                # Add the data to the current section's dataset
                dataset.append(line.split(','))
        # Don't forget to import the last section's data
        if current_resource:
            result = current_resource().import_data(dataset, dry_run=True)
            if not result.has_errors():
                current_resource().import_data(dataset, dry_run=False)
        return redirect("..")
    else:
        form = CSVUploadForm()
        return render(request, "admin/csv_form.html", {'form': form})