
import dash
import base64

from dash import html, dcc
import dash_bootstrap_components as dbc
from pages import navigation


dash.register_page(__name__, path = '/help')

font_style = 'Helvetica'

faq_trees = './assets/faq_phylos.png'
trees_base64 = base64.b64encode(open(faq_trees, 'rb').read()).decode('ascii')

faq_loading = './assets/faq_loading.png'
loading_base64 = base64.b64encode(open(faq_loading, 'rb').read()).decode('ascii')


layout = html.Div([
    navigation.navbar,
    html.Div([
        html.H3('FAQ'),
        dbc.Accordion([
                dbc.AccordionItem(
                    [
                        dcc.Markdown(''' These are the same trees with the 
                        difference being rotation of some of the branches, see 
                        figure below. Currently, only the **'...ladderTree.nw'** 
                        file is supported in combination with the operon plot, 
                        however it is still possible to upload and view 
                        the **'...tree.nw** file'.''',
                        style = {'fontFamily': font_style}),
                        html.Div(
                            html.Img(src='data:image/png;base64,{}'.format(trees_base64),
                                    style = {
                                        'height': '60%',
                                        'width': '60%',
                                        'position': 'center'}), 
                            style = {'textAlign': 'center'})
                    ],
                    title = ''' What is the difference between 
                    '...ladderTree.nw' and '...tree.nw'? ''',
                    style = {'fontFamily': font_style}
                ),
                dbc.AccordionItem(
                    [
                        html.P('''Hovering over the node should display the 
                        node label, otherwise try re-loading the page. If the 
                        issue still remians please contact us.'''),
                    ],
                    title = '''My phylogenetic tree is missing node labels''',
                ),
                dbc.AccordionItem(
                    '''Yes! Hover close to the right upper corner of the plot 
                    to display the toolbar. Click on the camera icon to 
                    download your plot in a .svg format''',
                    title = 'Can I download the plots?',
                ),
                dbc.AccordionItem([
                    dcc.Markdown( '''Longer query lists (>100 quries) can take 
                    longer to load, > 10s depending on legnth. To troubleshoot 
                    for application responsivness check if the browser tab is 
                    **'Updating...'**. If your plot is still not displaying, 
                    contact us.'''),
                    html.Div(
                        html.Img(src='data:image/png;base64,{}'.format(loading_base64),
                                style = {
                                    'height': '30%',
                                    'width': '30%',
                                    'position': 'center'}), 
                        style = {'textAlign': 'center'})],
                title = 'My operon plot is not displaying',
                ),
        ], start_collapsed = True)
    ], style = {
        'margin-left' : '250px', 
        'margin-top' : '60px',
        'margin-bottom' : '5px',
        'postion': 'relative',
        'width': '70%' }),
    html.Div([
        dbc.Card([
            dbc.CardHeader('Contact us'),
            dbc.CardBody(
                dcc.Markdown('''This is the first version of the 
                application and we expect bugs. If you experience 
                any issues, or have suggestions for imporvements and new 
                features e-mail us at **veda.bojar@med.lu.se**'''))
        ])    
    ], style = {
        'margin-left' : '250px', 
        'margin-top' : '60px',
        'postion': 'relative',
        'width': '70%' })
])

