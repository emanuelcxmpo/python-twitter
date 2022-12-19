import tweepy
from credentials import api
import dash
from dash import html
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
from dash_iconify import DashIconify
import plotly_express as px
import pandas as pd
from pymongo import MongoClient


app = dash.Dash(__name__, suppress_callback_exceptions=True)
app.title = "Pytweets"

app.layout = html.Div([
    html.Div([
        html.Nav([
            html.Ul([
                html.Li([
                    html.A([
                        DashIconify(icon="ion:logo-twitter"),
                    ], href=""),
                ], className='navbar-brand'),

                html.Li([
                    html.A([
                        DashIconify(icon="ion:home-outline"),
                    ], href="", className="item-icon home"),

                    html.A(["Home"], href="",
                           className="item-link"),
                ], className='nav-item'),

                html.Li([
                    html.A([
                        "#"], className="item-icon hash"),

                    html.A(["Explore"], href="",
                           className="item-link"),
                ], className='nav-item'),

                html.Li([
                    html.A([
                        DashIconify(icon="ion:notifications-outline"),
                    ], href="", className="item-icon"),

                    html.A(["Notification"], href="",
                           className="item-link"),
                ], className='nav-item'),

                html.Li([
                    html.A([
                        DashIconify(icon="ion:mail-outline"),
                    ], href="", className="item-icon"),

                    html.A(["Messages"], href="",
                           className="item-link"),
                ], className='nav-item'),

                html.Li([
                    html.A([
                        DashIconify(icon="ion:bookmark-outline"),
                    ], href="", className="item-icon"),

                    html.A(["Bookmarks"], href="",
                           className="item-link"),
                ], className='nav-item'),

                html.Li([
                    html.A([
                        DashIconify(icon="ion:reader-outline"),
                    ], href="", className="item-icon"),

                    html.A(["Lists"], href="", className="item-link"),
                ], className='nav-item'),

                html.Li([
                    html.A([
                        DashIconify(icon="ion:person-outline"),
                    ], href="", className="item-icon"),

                    html.A(["Profile"], href="",
                           className="item-link"),
                ], className='nav-item'),

                html.Li([
                    html.A([
                        DashIconify(
                            icon="ion:ellipsis-horizontal-circle-outline"),
                    ], href="", className="item-icon"),

                    html.A(["More"], href="", className="item-link"),
                ], className='nav-item'),

                html.A([
                    html.Div(["Tweet"], className="text")], href="", className='tweet-btn')
            ], className='navbar'),

            # Profile

            html.A([
                html.Div([
                    html.Img(src="https://i.postimg.cc/SNsDPvkK/DSC-0218-4c-min.jpg",
                             className="user-image"),
                    html.Div([
                        html.Span(["Emanuel Campo"], className="name"),
                        html.Span(["@emanuelcxmpo"], className="username")
                    ], style={"display": "flex", "flexDirection": "column"})
                ], className="profile-info"),

                html.Div([
                    DashIconify(icon="ion:ellipsis-horizontal"),
                ], className="option-icon")
            ], className="profile-btn")
        ], className='sidebar'),

        html.Section([
            html.Div([
                html.H3(["Home"], style={
                    "fontSize": "20px", "fontWeight": "bold", "color": "white"}),
                DashIconify(icon="ion:sparkles-outline",
                            style={"fontSize": "20px", "color": "white"})
            ], style={"display": "flex", "alignItems": "center", "width": "90%", "justifyContent": "space-between", "padding": "20px 0px 0px 0px"}),

            html.Div([
                html.Div([
                    html.Div([
                        html.Div([
                            html.Img(src="", className="profile-img",
                                     style={"width": "60px", "borderRadius": "99px"}, id="foto"),
                            html.Div([
                                html.Span(children="",
                                          id="nombre", className="user"),
                                html.Span(children="", className="username",
                                          id="usuario")
                            ], className="profile-user", style={"display": "grid"})
                        ], className="user-wrapper"),
                        html.Span(["Follow"], className="follow",)
                    ], className="row-top"),

                    html.P(children="", className="profile-bio", id="estado"),

                    html.Div([
                        html.Span([
                            DashIconify(icon="ion:location-outline",
                                        style={"fontSize": "20px", "marginRight": "5px"})
                        ], className="profile-items"),

                        html.Span(children="",
                                  className="profile-location", id="ubicacion"),

                        html.Span([
                            DashIconify(icon="ion:calendar-outline",
                                        style={"fontSize": "20px", "marginRight": "5px"})
                        ], className="profile-items"),

                        html.Span(children="",
                                  className="profile-location", id="creacion"),
                    ], className="row-middle"),

                    html.Div([
                        html.Span([
                            "Followers",
                            html.Span(children="0",
                                  className="count-meta", id="seguidores")
                        ], className="followers-count"),

                        html.Span([
                            "Following",
                            html.Span(children="0",
                                  className="count-meta", id="seguidos"),
                        ], className="following-count"),

                        html.Span([
                            "Likes",
                            html.Span(children="0",
                                  className="count-meta", id="megustas")
                        ], className="likes-count")
                    ], className="row-bottom")
                ], className="twitter-card")
            ], className="card"),

            # Card impresion de tweets
            html.Div([
                html.Div(id='listat')
            ], className="twitter-card-two"),
        ], className="section_tweets"),

        html.Div([
            html.Div([
                html.Label([
                    DashIconify(icon="ion:search-outline",
                                id="buscar", className="search_i")
                ], style={"display": "flex"}),

                dcc.Input(id='busqueda', value='', type="text",
                          placeholder='Ingrese el usuario incluyendo el @', className="input"),

                html.Div([
                    html.Button('Buscar', id='btn-click',
                                n_clicks=1, className="button_search")
                ])
            ], className="search"),

            html.Div([
                dbc.Col(
                    [dcc.Graph(id="grafica_one", figure=px.bar(template="plotly_dark"))])
            ], className="graph"),

            html.Div([
                dbc.Row(
                    [dbc.Col([dcc.Graph(id="grafica_two", figure=px.bar(template="plotly_dark"))])]),
            ], className="graph"),

            html.Div([
                dbc.Col(
                    [dcc.Graph(id="grafica_three", figure=px.bar(template="plotly_dark"))])
            ], className="graph")
        ], className="side-right"),
    ], className="body"),

    # Otra pagina
    html.Div([
        html.Nav([
            html.Ul([
                html.Li([
                    html.A([
                        DashIconify(icon="ion:logo-twitter"),
                    ], href=""),
                ], className='navbar-brand'),

                html.Li([
                    html.A([
                        DashIconify(icon="ion:home-outline"),
                    ], href="", className="item-icon home"),

                    html.A(["Home"], href="",
                           className="item-link"),
                ], className='nav-item'),

                html.Li([
                    html.A([
                        "#"], className="item-icon hash"),

                    html.A(["Explore"], href="",
                           className="item-link"),
                ], className='nav-item'),

                html.Li([
                    html.A([
                        DashIconify(icon="ion:notifications-outline"),
                    ], href="", className="item-icon"),

                    html.A(["Notification"], href="",
                           className="item-link"),
                ], className='nav-item'),

                html.Li([
                    html.A([
                        DashIconify(icon="ion:mail-outline"),
                    ], href="", className="item-icon"),

                    html.A(["Messages"], href="",
                           className="item-link"),
                ], className='nav-item'),

                html.Li([
                    html.A([
                        DashIconify(icon="ion:bookmark-outline"),
                    ], href="", className="item-icon"),

                    html.A(["Bookmarks"], href="",
                           className="item-link"),
                ], className='nav-item'),

                html.Li([
                    html.A([
                        DashIconify(icon="ion:reader-outline"),
                    ], href="", className="item-icon"),

                    html.A(["Lists"], href="", className="item-link"),
                ], className='nav-item'),

                html.Li([
                    html.A([
                        DashIconify(icon="ion:person-outline"),
                    ], href="", className="item-icon"),

                    html.A(["Profile"], href="",
                           className="item-link"),
                ], className='nav-item'),

                html.Li([
                    html.A([
                        DashIconify(
                           icon="ion:ellipsis-horizontal-circle-outline"),
                    ], href="", className="item-icon"),

                    html.A(["More"], href="", className="item-link"),
                ], className='nav-item'),

                html.A([
                    html.Div(["Tweet"], className="text")], href="", className='tweet-btn')
            ], className='navbar'),

            # Profile

            html.A([
                html.Div([
                    html.Img(src="https://i.postimg.cc/SNsDPvkK/DSC-0218-4c-min.jpg",
                             className="user-image"),
                    html.Div([
                        html.Span(["Emanuel Campo"], className="name"),
                        html.Span(["@emanuelcxmpo"], className="username")
                    ], style={"display": "flex", "flexDirection": "column"})
                ], className="profile-info"),

                html.Div([
                    DashIconify(icon="ion:ellipsis-horizontal"),
                ], className="option-icon")
            ], className="profile-btn")
        ], className='sidebar'),

        html.Section([
            html.Div([
                html.H3(["Explore"], style={
                    "fontSize": "20px", "fontWeight": "bold", "color": "white"}),
                DashIconify(icon="ion:settings-outline",
                            style={"fontSize": "20px", "color": "white"})
            ], style={"display": "flex", "alignItems": "center", "width": "90%", "justifyContent": "space-between", "padding": "20px 0px 20px 0px"}),

            html.Div([
                html.Div([
                    html.Label([
                        DashIconify(icon="ion:search-outline",
                                    id="buscar-hashtag", className="search_i")
                    ], style={"display": "flex"}),

                    dcc.Input(id='busqueda-hashtag', value='', type="text",
                              placeholder='Ingrese el hashtag del tema incluyendo el #', className="input"),

                    html.Div([
                        html.Button('Buscar', id='btn-hashtag',
                                    n_clicks=1, className="button_search")
                    ])
                ], className="search-one"),
            ]),

            # Card tweet hashtag
            html.Div([
                html.Div(id='listat-hashtag')
            ], className="twitter-card-two"),
        ], className="section-tweets-one"),
    ], className="body"),
])

# Realiza la extracción de tweet segun el usuario


@ app.callback(
    [Output('foto', 'src')],
    [Output('nombre', 'children')],
    [Output('usuario', 'children')],
    [Output('estado', 'children')],
    [Output('ubicacion', 'children')],
    [Output('creacion', 'children')],
    [Output('seguidores', 'children')],
    [Output('seguidos', 'children')],
    [Output('megustas', 'children')],
    # ---------------------------------
    [Output('grafica_one', 'figure')],
    [Output('grafica_two', 'figure')],
    [Output('grafica_three', 'figure')],
    [Output('listat', 'children')],
    [Input('btn-click', 'n_clicks')],
    [State('busqueda', 'value')],
    prevent_initial_call=True
)
def mostrar(n_clincks, usuario):
    twee = []
    if n_clincks > 1:

        tweets = tweepy.Cursor(api.user_timeline, screen_name=usuario,
                               count=200,
                               include_rts=False,
                               tweet_mode='extended').items(100)

        for tweet in tweets:
            twee.append([tweet.user.screen_name, tweet.full_text, tweet.favorite_count,
                         tweet.retweet_count, tweet.created_at.year])
        colum = ['usuario', 'texto', 'like', 'retweets', 'fecha']

        followers = []
        colum1 = ['seguidores', 'fecha']
        for follower in tweepy.Cursor(api.get_followers, screen_name=usuario, count=200).items(100):
            followers.append([follower.screen_name, follower.created_at.year])
        fll = pd.DataFrame(followers, columns=colum1)

        df = pd.DataFrame(twee, columns=colum)

        # Guardar en un archivo
        df.to_csv("user.csv")

        data = df.to_dict(orient="record")

        # Conexión a base de datos
        def connect_db():
            client = MongoClient("localhost", 27017)
            return client

        # Guardar en base de datos
        client = connect_db()
        db = client.Data_extraction
        print(db)
        db.user.insert_many(data)

        foto = tweet.user.profile_image_url
        nombre = tweet.user.name
        estado = tweet.user.description
        creacion = tweet.user.created_at.month

        if creacion == 1:
            creacion = "January"
        elif creacion == 2:
            creacion = "Febrary"
        elif creacion == 3:
            creacion = "March"
        elif creacion == 4:
            creacion = "April"
        elif creacion == 5:
            creacion = "May"
        elif creacion == 6:
            creacion = "June"
        elif creacion == 7:
            creacion = "July"
        elif creacion == 8:
            creacion = "August"
        elif creacion == 9:
            creacion = "September"
        elif creacion == 10:
            creacion = "October"
        elif creacion == 11:
            creacion = "November"
        else:
            creacion = "December"

        new_creacion = str("Joined ") + str(creacion) + \
            "  " + str(tweet.user.created_at.year)

        ubicacion = tweet.user.location
        seguidores_one = tweet.user.followers_count
        seguidos = tweet.user.friends_count
        megustas = df["like"].sum()

        if ubicacion == "":
            ubicacion = "Ubicación no disponible"

        # Grafica cantidad de seguidores al año
        numfollowers = fll.groupby(['fecha'], as_index=False)[
            ['seguidores']].count()
        grafica_uno = px.bar(data_frame=numfollowers, x="fecha", y="seguidores",
                             color="fecha", title="Cantidad de seguidores por año", template="plotly_dark")

        # Grafica cantidad de tweets realizados al año
        numtweets = df.groupby(["fecha"], as_index=False)[["texto"]].count()
        grafica_dos = px.bar(data_frame=numtweets, x="fecha", y="texto",
                             color="fecha", title="Cantidad de tweets realizados al año", template="plotly_dark")

        # Grafica cantidad de likes recibidos al año
        numlikes = df.groupby(["fecha"], as_index=False)[["like"]].sum()
        grafica_tres = px.bar(data_frame=numlikes, x="fecha", y="like",
                              color="fecha", title="Cantidad de likes obtenidos por año", template="plotly_dark")

        tww = tweepy.Cursor(api.user_timeline, screen_name=usuario,
                            count=200,
                            include_rts=False,
                            tweet_mode='extended').items(100)

        return foto, nombre, usuario, estado, ubicacion, new_creacion, seguidores_one, seguidos, megustas, grafica_uno, grafica_dos, grafica_tres,  [html.Ul(id='my-list', children=[html.Li([html.Div([html.Img(src=i.user.profile_image_url,
                                                                                                                                                                                                                 className="twitter-content-image", id="foto_user_tweet"),
                                                                                                                                                                                                        html.Div([
                                                                                                                                                                                                            html.A(children=i.user.name,
                                                                                                                                                                                                                   className="twitter-card-name", id="nombre_user_tweet"),

                                                                                                                                                                                                            html.A(children="@" + i.user.screen_name,
                                                                                                                                                                                                                   className="twitter-card-user", id="usuario_user_tweet"),

                                                                                                                                                                                                            html.A(children=str(i.created_at.day) + " - " + str(i.created_at.month) + " - " + str(i.created_at.year),
                                                                                                                                                                                                                   className="twitter-card-info", id="fecha_tweet"),

                                                                                                                                                                                                            html.Div([
                                                                                                                                                                                                                 html.A(children=i.full_text,
                                                                                                                                                                                                                        className="twitter-card-text", id="texto_tweet"),
                                                                                                                                                                                                                 ], className="twitter-card-tweet"),

                                                                                                                                                                                                            html.Div([
                                                                                                                                                                                                                DashIconify(
                                                                                                                                                                                                                     icon="ion:chatbubble-outline"),
                                                                                                                                                                                                                html.A(children=[], className="twitter-card-icon",
                                                                                                                                                                                                                       id="comentarios"),

                                                                                                                                                                                                                DashIconify(
                                                                                                                                                                                                                    icon="ion:sync-outline"),
                                                                                                                                                                                                                html.A(children=i.retweet_count, className="twitter-card-icon",
                                                                                                                                                                                                                       id="retweet"),

                                                                                                                                                                                                                DashIconify(
                                                                                                                                                                                                                    icon="ion:heart-outline"),
                                                                                                                                                                                                                html.A(children=i.favorite_count, className="twitter-card-icon",
                                                                                                                                                                                                                       id="likes_tweets"),

                                                                                                                                                                                                                html.A([
                                                                                                                                                                                                                    DashIconify(
                                                                                                                                                                                                                        icon="ion:share-outline"),
                                                                                                                                                                                                                ], className="twitter-card-icon")
                                                                                                                                                                                                            ], className="twitter-card-icons")
                                                                                                                                                                                                        ], className="twitter-card-content")
                                                                                                                                                                                                        ], className="twitter-card-one")]) for i in tww])]
    else:
        return {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}


# Inicia la extracción de tweet que contengan cierto hashtag
@app.callback(
    [Output('listat-hashtag', 'children')],
    [Input('btn-hashtag', 'n_clicks')],
    [State('busqueda-hashtag', 'value')],
    prevent_initial_call=True
)
def extraccion(n_clincks, words):
    if n_clincks > 1:
        tweets = tweepy.Cursor(api.search_tweets, q=words,
                               lang="es", tweet_mode='extended').items(100)

        return [html.Ul(id='my-list-hashtag', children=[html.Li([html.Div([html.Img(src=i.user.profile_image_url,
                                                                                    className="twitter-content-image", id="foto_user_tweet_hastag"),
                                                                           html.Div([
                                                                               html.A(children=i.user.name,
                                                                                      className="twitter-card-name", id="nombre_user_tweet_hastag"),

                                                                               html.A(children="@" + i.user.screen_name,
                                                                                      className="twitter-card-user", id="usuario_user_tweet_hastag"),

                                                                               html.A(children=str(i.created_at.month) + " - " + str(i.created_at.year),
                                                                                      className="twitter-card-info", id="fecha_tweet_hastag"),

                                                                               html.Div([
                                                                                   html.A(children=i.full_text,
                                                                                          className="twitter-card-text", id="texto_tweet_hastag"),
                                                                               ], className="twitter-card-tweet"),

                                                                               html.Div([
                                                                                   DashIconify(
                                                                                       icon="ion:chatbubble-outline"),
                                                                                   html.A(children=[], className="twitter-card-icon",
                                                                                          id="comentarios_hastag"),

                                                                                   DashIconify(
                                                                                       icon="ion:sync-outline"),
                                                                                   html.A(children=i.retweet_count, className="twitter-card-icon",
                                                                                          id="retweet_hastag"),

                                                                                   DashIconify(
                                                                                       icon="ion:heart-outline"),
                                                                                   html.A(children=i.favorite_count, className="twitter-card-icon",
                                                                                          id="likes_tweets_hastag"),

                                                                                   html.A([
                                                                                       DashIconify(
                                                                                           icon="ion:share-outline"),
                                                                                   ], className="twitter-card-icon")
                                                                               ], className="twitter-card-icons")
                                                                           ], className="twitter-card-content")
                                                                           ], className="twitter-card-one")]) for i in tweets])]

    else:
        return {}


if __name__ == "__main__":
    app.run_server(debug=True)
