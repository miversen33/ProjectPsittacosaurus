from flask import render_template, request, current_app as app, session, json, url_for

_TEMPLATE = '_player_generation.html'

    # {'route': '/_player_generation', 'endpoint': player_generation_page, IS_INTERNAL: True},
@app.route('/_player_generation', is_internal=True)
def generation_page():

    page_data = dict(
        positions=['Quarterback'],
    )
    return render_template(_TEMPLATE, **page_data)

def position_info_lookup():
    return ""