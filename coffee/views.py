from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from coffee.forms import authForm, DateRangeForm
from coffee.models import *
from django.contrib.auth.decorators import login_required
from coffee.scripts.monthSales import monthSales
from coffee.scripts.bestPlaces import bestPlaces
from coffee.scripts.topMenu import topMenu
from coffee.scripts.popMenu import popMenu
from coffee.static.coffee import *
from django.db.models import Q
import io
from django.core.files.base import ContentFile
import matplotlib.pyplot as plt
import base64
from django.shortcuts import render
from .forms import DateRangeForm
from .models import ReportArchive
from .scripts.pred_a import predict_a
from .scripts.pred_b import predict_b
from .scripts.pred_c import predict_c
from .scripts.pred_d import predict_d
import csv

archive = [
    {
        'date': "Время еще не настало",
        'description':'Этот раздел находится в разработке. Следите за новостями!'
   },
     {
        'date': "Время еще не настало",
        'description':'Этот раздел находится в разработке. Следите за новостями!'
   },
     {
        'date': "Время еще не настало",
        'description':'Этот раздел находится в разработке. Следите за новостями!'
        }
]
def index_view(request):
    user = User.objects.get(id=1)
    return HttpResponse(str(user.profile.phone_number))

def auth(request):
    if request.method == "POST":
        form = authForm(request.POST)
        u_name = request.POST.get("username")
        u_pass = request.POST.get("password")
        user = authenticate(username=u_name, password=u_pass)
        if user is not None:
            login(request, user)
            return redirect('main-window')
        else:
            return render(request, "coffee/authorization.html", {"form":form, "form_err":form.error_messages})
    else:
        form = authForm()
        return render(request, "coffee/authorization.html", {"form":form, "form_err":None})

@login_required
def main(request):
    context = {
                'archive':archive,
            }
    return render(request, "coffee/main.html", context)

@login_required
def guide(request):
    return render(request, "coffee/guide.html")

@login_required
def guideMetrics(request):
    return render(request, "coffee/guideMetrics.html")

@login_required
def workarchive(request):
    reports = ReportArchive.objects.filter(created_by=request.user)
    report_type = request.GET.get('report_type')
    if report_type:
        reports = reports.filter(report_type=report_type)

    search_query = request.GET.get('q')
    if search_query:
        reports = reports.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query))

    sort_order = request.GET.get('sort', 'desc') 
    if sort_order == 'asc':
        reports = reports.order_by('created_at')
    else:
        reports = reports.order_by('-created_at')

    return render(request, 'coffee/archive.html', {'reports': reports})
   
@login_required
def profile(request):
    context = {
    }
    return render(request, "coffee/profile.html", context)

@login_required
def profileMetrics(request):
    return render(request, "coffee/profileMetrics.html")

@login_required
def mlmodel(request, id):
    mlmodel = get_object_or_404(MLModel, pk=id)

    start_date = None
    end_date = None
    forecast_summary = chart_labels = chart_values = None
    forecast_list = None
    all_locations = []

    if mlmodel.id == 1:
        import os
        import pandas as pd
        current_dir = os.path.join(os.path.dirname(__file__), 'scripts')
        csv_path = os.path.join(current_dir, 'coffee_sales.csv')
        df = pd.read_csv(csv_path)
        all_locations = sorted(df['location'].unique())

        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date") or start_date
            location_filter = request.POST.getlist("locations")

            result = predict_a(start_date, end_date, location_filter)
            forecast_summary = result["summary"]
            chart_labels = result["chart_data"]["labels"]
            chart_values = result["chart_data"]["values"]

    elif mlmodel.id == 2:
        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date") or start_date

            result = predict_b(start_date, end_date)
            forecast_list = result["summary_list"]
            chart_labels = result["chart_data"]["labels"]
            chart_values = result["chart_data"]["datasets"]

    elif mlmodel.id == 3:
        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date") or start_date

            result = predict_c(start_date, end_date)
            forecast_summary = result["summary"]
            chart_labels = result["chart_data"]["labels"]
            chart_values = result["chart_data"]["values"]

    elif mlmodel.id == 4:
        if request.method == 'POST':
            start_date = request.POST.get("start_date")
            end_date = request.POST.get("end_date") or start_date

            result = predict_d(start_date, end_date)
            forecast_list = result["summary_list"]
    table_base64 = None
    graph_base64 = None
    if mlmodel.id in [2, 4] and forecast_list:
        text_data = "\n".join(str(line) for line in forecast_list)
        table_base64 = base64.b64encode(text_data.encode("utf-8")).decode("utf-8")

    if mlmodel.id in [1, 3] and chart_labels and chart_values:
        graph_base64 = "placeholder"
    return render(request, 'coffee/mlmodel.html', {
    'mlmodel': mlmodel,
    'forecast_summary': forecast_summary,
    'forecast_list': forecast_list,
    'chart_labels': chart_labels,
    'chart_values': chart_values,
    'start_date': start_date,
    'end_date': end_date,
    'all_locations': all_locations,
    'table': table_base64,
    'graph': graph_base64
})

@login_required
def metric(request, id):
    form = DateRangeForm(request.GET or None)
    metric = Metric.objects.get(pk=id)

    if form.is_valid():
        start_date = form.cleaned_data['start_date']
        end_date = form.cleaned_data['end_date']
    else:
        start_date = '2022-01-01'
        end_date = '2025-01-01'

    if metric.id == 1:
        graph_base64, table_base64 = bestPlaces(start_date, end_date)
    elif metric.id == 2:
        graph_base64, table_base64 = monthSales(start_date, end_date)
    elif metric.id == 3:
        graph_base64, table_base64 = topMenu(start_date, end_date)
    else:
        graph_base64, table_base64 = popMenu(start_date, end_date)

    context = {
        'form': form,
        'metric': metric,
        'graph': graph_base64,
        'table': table_base64,  
    }

    return render(request, "coffee/metric.html", context)

@login_required
def save_to_archive(request):
    if request.method == 'POST':
        graph_data = request.POST.get('graph_base64')
        table_data = request.POST.get('table_base64')  
        forecast_text = request.POST.get('forecast_content') 
        model_id = request.POST.get('mlmodel_id') 
        metric_name = request.POST.get('metric_name') or request.POST.get('report_title', 'Без названия')
        metric_description = request.POST.get('metric_description') or request.POST.get('report_description', '')
        report_type = request.POST.get('report_type', 'forecast')

        if model_id:
            model_id = int(model_id)
            if model_id in [1, 3] and graph_data and graph_data.startswith("data:image"):
                graph_file = ContentFile(base64.b64decode(graph_data.split(",")[1]), name=f"{metric_name}_graph.png")
                ReportArchive.objects.create(
                    title=f"Прогноз-график: {metric_name}",
                    description=metric_description,
                    report_type='forecast',
                    file=graph_file,
                    filters=None,
                    created_by=request.user
                )
                return redirect('archive')

            if model_id in [2, 4] and table_data:
                table_file = ContentFile(base64.b64decode(table_data), name=f"{metric_name}_report.txt")
                ReportArchive.objects.create(
                    title=f"Прогноз-отчёт: {metric_name}",
                    description=metric_description,
                    report_type='forecast',
                    file=table_file,
                    filters=None,
                    created_by=request.user
                )
                return redirect('archive')

        if graph_data and graph_data.startswith("data:image"):
            graph_file = ContentFile(base64.b64decode(graph_data.split(",")[1]), name=f"{metric_name}_graph.png")
            ReportArchive.objects.create(
                title=f"График: {metric_name}",
                description=metric_description,
                report_type='graph',
                file=graph_file,
                filters=None,
                created_by=request.user
            )

        if table_data:
            table_file = ContentFile(base64.b64decode(table_data), name=f"{metric_name}_report.txt")
            ReportArchive.objects.create(
                title=f"Отчёт: {metric_name}",
                description=metric_description,
                report_type='forecast',
                file=table_file,
                filters=None,
                created_by=request.user
            )

        if forecast_text:
            txt_file = ContentFile(forecast_text.encode("utf-8"), name=f"{metric_name}_forecast.txt")
            ReportArchive.objects.create(
                title=f"Прогноз: {metric_name}",
                description=metric_description,
                report_type='forecast',
                file=txt_file,
                filters=None,
                created_by=request.user
            )

    return redirect('archive')

def logOutView(request):
    logout(request)
    return redirect("authorization")

@login_required
def render_forecast(request, model_func, model_name, model_id):
    forecast_summary = None
    graph_base64 = None
    table_base64 = None
    forecast_list = None
    print(">>> render_forecast called") 
    if request.method == "POST":
        start_date = request.POST.get("start_date")
        end_date = request.POST.get("end_date") or start_date

        if start_date:
            result = model_func(start_date, end_date)

            if model_id in [1, 3] and isinstance(result, tuple):
                fig, summary = result
                buf = io.BytesIO()
                fig.savefig(buf, format="png")
                buf.seek(0)
                graph_base64 = "data:image/png;base64," + base64.b64encode(buf.read()).decode("utf-8")
                plt.close(fig)
                forecast_summary = summary

            elif model_id in [2, 4] and isinstance(result, list):
                forecast_list = result
                if forecast_list:
                    forecast_text = "\n".join(str(line) for line in forecast_list)
                    table_base64 = base64.b64encode(forecast_text.encode("utf-8")).decode("utf-8")
                    print("✅ table_base64 generated:", table_base64[:50])
                else:
                    print("⚠️ forecast_list пустой — не сериализуем")

    return render(request, "coffee/mlmodel.html", {
        "mlmodel": {"name": model_name, "id": model_id, "quality": 92.5},
        "forecast_summary": forecast_summary,
        "forecast_list": forecast_list,
        "graph": graph_base64,
        "table": table_base64,
    })
