'''
Penalty
    id      (Integer, Primary, Indexed),
    penalty_id (Integer, ForeignKey PenaltyDetails(id), Indexed),
    play_state (Integer, ForeignKey PlayState(id), Indexed)

PenaltyDetails
    id             (Integer, Primary, Indexed)
    description    (String)
    yards_assessed (Integer, default=-1)
    loss_of_down   (Boolean, default=False)
    details        (String) -- If the penalty doesn't fit any of the other columns, place its details here and parse them on the server
'''