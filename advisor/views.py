from django.shortcuts import render
from .forms import FinancialAdviceForm
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from .logic import FinancialAdvisor

def generate_chart(data):
    labels = [item['name'] for item in data]
    sizes = [item['value'] for item in data]
    
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    plt.close()
    buffer.seek(0)
    
    image_png = buffer.getvalue()
    buffer.close()
    
    return base64.b64encode(image_png).decode('utf-8')

def index(request):
    if request.method == 'POST':
        form = FinancialAdviceForm(request.POST)
        if form.is_valid():
            advisor = FinancialAdvisor()
            result = advisor.get_financial_advice(
                age=form.cleaned_data['age'],
                gender=form.cleaned_data['gender'],
                objective=form.cleaned_data['objective'],
                factor=form.cleaned_data['factor'],
                duration=form.cleaned_data['duration'],
                expect=form.cleaned_data['expect'],
                avenue=form.cleaned_data['avenue']
            )
            
            # Generate chart data
            # chart_data = [
            #     {'name': 'Equities', 'value': 60},
            #     {'name': 'Fixed Income', 'value': 30},
            #     {'name': 'Alternatives', 'value': 10}
            # ]
            
            # chart_image = generate_chart(chart_data)
            
            return render(request, 'advisor/results.html', {
                'form_data': form.cleaned_data,
                'advice': result['advice'],
                # 'chart_image': chart_image,
                'similar_profiles': result['similar_profiles']
            })
    else:
        form = FinancialAdviceForm()
    
    return render(request, 'advisor/index.html', {'form': form})