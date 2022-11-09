import dash
from dash import html

import dash_bootstrap_components as dbc


navbar = dbc.Navbar(
    dbc.Container([
        dbc.Row([
            dbc.Col(
                dbc.NavbarBrand('FlaGs Visualisation', className="ms-2")),
            dbc.Col(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("Home", href = "/")),
                    dbc.NavItem(dbc.NavLink("Help", href = "/help"))
                ], navbar = True),
            width = {'size': 'auto'})],
        align = 'center', 
        className = 'g-0'),
        dbc.Row([
            dbc.Col([
                dbc.Nav([
                    dbc.NavItem(
                        dbc.NavLink(
                            html.I(className = 'bi bi-flag-fill'),
                            href = """http://webflags.se/""",
                            external_link = True)),
                    dbc.NavItem(
                        dbc.NavLink(
                            html.I(className = 'bi bi-github'),
                                href = """https://github.com/GCA-VH-lab""",
                                external_link = True)),
                    dbc.NavItem(
                        dbc.NavLink(
                            html.I(className = 'bi bi-twitter'),
                                href = """https://twitter.com/webflags1?ref_src=twsrc%5Etfw%7Ctwcamp%5Eembeddedtimeline%7Ctwterm%5Escreen-name%3Awebflags1%7Ctwcon%5Es2""",
                                external_link = True))
                ], navbar = True)
            ])
        ], align = 'center')
    ], fluid = True),
    color = 'rgb(52,58,64)',
    dark = True)