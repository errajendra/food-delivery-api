from django.shortcuts import render, redirect
# from datetime import datetime, date

def update_confi_setting(request):
    from django.conf import settings
    from constance.admin import ConstanceAdmin, ConstanceForm, Config, get_values
    from django.utils.translation import gettext_lazy as _
    from constance import config
    initial = get_values()
    if request.method == 'GET':
        form = ConstanceForm(initial=initial)
        fieldsets = []
        for fieldset_title, fieldset_data in settings.CONSTANCE_CONFIG_FIELDSETS.items():
            if type(fieldset_data) == dict:
                fields_list = fieldset_data['fields']
                collapse = fieldset_data.get('collapse', False)
            else:
                fields_list = fieldset_data
                collapse = False

            absent_fields = [field for field in fields_list
                            if field not in settings.CONSTANCE_CONFIG]
            assert not any(absent_fields), (
                "CONSTANCE_CONFIG_FIELDSETS contains field(s) that does "
                "not exist: %s" % ', '.join(absent_fields))

            config_values = []

            for name in fields_list:
                options = settings.CONSTANCE_CONFIG.get(name)
                if options:
                    default, help_text = options[0], options[1]
                    value = initial.get(name)
                    config_values.append(
                        {
                            'name': name,
                            'default': default,
                            'raw_default': default,
                            'help_text': _(help_text),
                            'value': value,
                            'modified': value != default,
                            'form_field': form[name],
                            # 'is_date': isinstance(default, date),
                            # 'is_datetime': isinstance(default, datetime),
                            # 'is_checkbox': isinstance(form[name].field.widget, forms.CheckboxInput),
                            # 'is_file': isinstance(form[name].field.widget, forms.FileInput),
                        }
                    )
            fieldset_context = {
                'title': fieldset_title,
                'config_values': config_values
            }

            fieldsets.append(fieldset_context)
        return render(
            request, 'setting/update-constance.html',
            {'config': config, 'form': form, 'fieldsets': fieldsets}
        )

    if request.method == 'POST':
        form = ConstanceForm(data=request.POST, initial=initial)
        if form.is_valid():
            form.save()
        return redirect('update-constance')
