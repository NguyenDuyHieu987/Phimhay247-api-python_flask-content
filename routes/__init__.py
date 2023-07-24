from flask import *


def route(app, cache):
    from routes.ErrorHandler import error_handler

    error_handler(app)

    # Movie slug
    from routes.MovieSlugRoutes import movie_slug_routes

    movie_slug_routes(app, cache)

    # Tv slug
    from routes.TvSlugRoutes import tv_slug_routes

    tv_slug_routes(app, cache)

    # Movie

    from routes.MovieRoutes import movie_routes

    movie_routes(app, cache)

    # Tv
    from routes.TvRoutes import tv_routes

    tv_routes(app, cache)

    # Tv seasons
    from routes.TvSeasonsRoutes import tv_seasons_routes

    tv_seasons_routes(app, cache)

    # Rating
    from routes.RatingRoutes import rating_routes

    rating_routes(app)

    # Update view
    from routes.UpdateViewRoutes import update_view_routes

    update_view_routes(app)

    # Comment
    from routes.CommentRoutes import comment_routes

    comment_routes(app)

    # Trending
    from routes.TrendingRoutes import trending_routes

    trending_routes(app, cache)

    # Search
    from routes.SearchRoutes import search_routes

    search_routes(app, cache)

    # Get sortby
    from routes.SortByRoutes import sortbys_routes

    sortbys_routes(app, cache)

    # Get genres
    from routes.GenresRoutes import genres_routes

    genres_routes(app, cache)

    # Get years
    from routes.YearsRoutes import years_routes

    years_routes(app, cache)

    # Get countries
    from routes.CountriesRoutes import countries_routes

    countries_routes(app, cache)

    # Discover
    from routes.DiscoverRoutes import discover_routes

    discover_routes(app, cache)

    # Similar
    from routes.SimilarRoutes import similar_routes

    similar_routes(app, cache)

    # Credits
    from routes.CreditsRoutes import credits_routes

    credits_routes(app, cache)

    # Images
    from routes.ImagesRoutes import images_routes

    images_routes(app, cache)

    # Videos
    from routes.VideosRoutes import videos_routes

    videos_routes(app, cache)

    # List
    from routes.ListRoutes import list_routes

    list_routes(app, cache)

    # History

    ## Get history
    from routes.HistoryRoutes import history_routes

    history_routes(app, cache)

    # Recommend (Suggest)

    ## Get Recommend
    from routes.RecommendRoutes import recommend_routes

    recommend_routes(app, cache)

    # Ranking
    from routes.RankingRoutes import ranking_routes

    ranking_routes(app, cache)

    # Authentication
    from routes.AuthenticationRoutes import authentication_routes

    authentication_routes(app)

    # Pricing
    from routes.PlansRoutes import plans_routes

    plans_routes(app, cache)
