'''
Rules -- Might be a reasonable idea to include the penalties in here? Maybe?
    id (Integer, Indexed, Primary),
    description (String),

LeagueRules
    id (Integer, Indexed, Primary),
    league_id (Integer, ForeignKey league(id), Indexed),
    rule_id (Integer, ForeingKey rules(id), Indexed),
    is_active (Boolean, default=True)
'''