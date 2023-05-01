def route(app):
    # Movie slug
    from routes.MovieSlugRoutes import movie_slug_routes

    movie_slug_routes(app)

    # Tv slug
    from routes.TvSlugRoutes import tv_slug_routes

    tv_slug_routes(app)

    # Movie

    from routes.MovieRoutes import movie_routes

    movie_routes(app)

    # Tv
    from routes.TvRoutes import tv_routes

    tv_routes(app)

    # Tv seasons
    from routes.TvSeasonsRoutes import tv_seasons_routes

    tv_seasons_routes(app)

    # Rating
    from routes.RatingRoutes import rating_routes

    rating_routes(app)

    # Trending
    from routes.TrendingRoutes import trending_routes

    trending_routes(app)

    # Search
    from routes.SearchRoutes import search_routes

    search_routes(app)

    # Get sortby
    from routes.SortByRoutes import sortbys_routes

    sortbys_routes(app)

    # Get genres
    from routes.GenresRoutes import genres_routes

    genres_routes(app)

    # Get years
    from routes.YearsRoutes import years_routes

    years_routes(app)

    # Get countries
    from routes.CountriesRoutes import countries_routes

    countries_routes(app)

    # Discover
    from routes.DiscoverRoutes import discover_routes

    discover_routes(app)

    # Similar
    from routes.SimilarRoutes import similar_routes

    similar_routes(app)

    # List
    from routes.ListRoutes import list_routes

    list_routes(app)

    # WatchList (View History)

    ## Get history
    from routes.WatchListRoutes import watchlist_routes

    watchlist_routes(app)

    # Recommend (Suggest)

    ## Get Recommend
    from routes.RecommendRoutes import recommend_routes

    recommend_routes(app)

    # Ranking
    from routes.RankingRoutes import ranking_routes

    ranking_routes(app)

    # Authentication
    from routes.AuthenticateRoutes import authenticate_routes

    authenticate_routes(app)
