from admin_module.forms import SubclassForm
from admin_module.models import Subclass
from django.shortcuts import redirect, render, get_object_or_404

def subclass(request):
    subclass_data = Subclass.objects.all()
    if request.method == 'POST':
        form = SubclassForm(request.POST)
        if form.is_valid():
            subclass = form.save(commit=False)
            subclass.created_by = request.user.username
            subclass.modified_by = request.user.username
            form.save()
        return redirect('admin_module:subclass')
    else:
        form = SubclassForm()

    return render(request, 'dictionaries/subclass.html', {'subclass_data': subclass_data, 'form': form,})


def edit_subclass(request, subclass_id):
    subclass = get_object_or_404(Subclass, pk=subclass_id)
    subclass_data = Subclass.objects.all()

    if request.method == 'POST':
        form = SubclassForm(request.POST, instance=subclass)
        if form.is_valid():
            subclass = form.save(commit=False)
            subclass.modified_by = request.user.username
            form.save()
            return redirect('admin_module:subclass')

    else:
        form = SubclassForm(instance=subclass)

    return render(request, 'dictionaries/edit_subclass.html',
                  {'subclass': subclass, 'form': form})


def delete_subclass(request, subclass_id):
    subclass = get_object_or_404(Subclass, pk=subclass_id)

    if request.method == 'POST':
        subclass.delete()
        return redirect('admin_module:subclass')

    return render(request, 'dictionaries/delete_subclass.html', {'subclass': subclass})
