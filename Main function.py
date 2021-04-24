import pandas as pd
import datetime
import numpy as np
import pytz
import math

#Import in data
games = pd.read_csv('games.csv')
players =pd.read_csv('players.csv')
plays =pd.read_csv('plays.csv')
week1 = pd.read_csv('week1.csv')
week2 = pd.read_csv('week2.csv')
week3 = pd.read_csv('week3.csv')
week4 = pd.read_csv('week4.csv')
week5 = pd.read_csv('week5.csv')
week6 = pd.read_csv('week6.csv')
week7 = pd.read_csv('week7.csv')
week8 = pd.read_csv('week8.csv')
week9 = pd.read_csv('week9.csv')
week10 = pd.read_csv('week10.csv')
week11 = pd.read_csv('week11.csv')
week12 = pd.read_csv('week12.csv')
week13 = pd.read_csv('week13.csv')
week14 = pd.read_csv('week14.csv')
week15 = pd.read_csv('week15.csv')
week16 = pd.read_csv('week16.csv')
week17 = pd.read_csv('week17.csv')

#Turn off time localization
week1['time'] = pd.to_datetime(week1['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week2['time'] = pd.to_datetime(week2['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week3['time'] = pd.to_datetime(week3['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week4['time'] = pd.to_datetime(week4['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week5['time'] = pd.to_datetime(week5['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week6['time'] = pd.to_datetime(week6['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week7['time'] = pd.to_datetime(week7['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week8['time'] = pd.to_datetime(week8['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week9['time'] = pd.to_datetime(week9['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week10['time'] = pd.to_datetime(week10['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week11['time'] = pd.to_datetime(week11['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week12['time'] = pd.to_datetime(week12['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week13['time'] = pd.to_datetime(week13['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week14['time'] = pd.to_datetime(week14['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week15['time'] = pd.to_datetime(week15['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week16['time'] = pd.to_datetime(week16['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)
week17['time'] = pd.to_datetime(week17['time'], format = '%Y-%m-%dT%H:%M:%S').dt.tz_localize(None)

#simple distance calculator that takes in x and y coordinates
def dist(pos1, pos2):
    val = math.sqrt((pos1[0]-pos2[0])**2 + (pos1[1]-pos2[1])**2)
    return val

#function that returns a dataframe of all defenders on a play, along with the nearest receiver and postion data
def Defender_dist(week, gameid, lst_playid):
    offense = ['RB', 'FB', 'WR', 'TE', 'HB']
    defense = ['SS','FS', 'MLB', 'CB', 'LB', 'OLB', 'ILB','DB', 'S']
    data = []
    for y in lst_playid:
      def_dict = {}
      off_dict = {}
      down_distance = plays.loc[(plays['gameId'] == gameid) & (plays['playId'] == y), ['down', 'yardsToGo']].values
      for x in defense:
        defense_data = week.loc[(week['gameId'] == gameid) & (week['playId'] == y) & (week['position'] == x),['x', 'y', 'position', 'displayName', 'o']].values #(week['event'] == 'pass_forward') & 
        if defense_data.shape[0] == 1:
          pos = defense_data[0][2]
          def_xy = defense_data[0][0:2]
          def_name = defense_data[0][3]
          def_o = defense_data[0][4]
          def_dict[def_name] = [def_xy, pos, def_o]
        elif defense_data.shape[0] == 0:
          pass
        else:
          for x in range(defense_data.shape[0]):
            pos = defense_data[x][2]
            def_xy = defense_data[x][0:2]
            def_name = defense_data[x][3]
            def_o = defense_data[x][4]
            def_dict[def_name] = [def_xy, pos, def_o]
      for x in offense:
        offense_data = week.loc[(week['gameId'] == gameid) & (week['playId'] == y) & (week['position'] == x),['x', 'y', 'position', 'displayName', 'o']].values  #(week['event'] == 'pass_forward') & 
        if offense_data.shape[0] == 1:
          pos = offense_data[0][2]
          off_xy = offense_data[0][0:2]
          off_name = offense_data[0][3]
          off_o = offense_data[0][4]
          off_dict[off_name] = [off_xy, pos, off_o]
        elif offense_data.shape[0] == 0:
          pass
        else:
          for x in range(offense_data.shape[0]):
            pos = offense_data[x][2]
            off_xy = offense_data[x][0:2]
            off_name = offense_data[x][3]
            off_o = offense_data[x][4]
            off_dict[off_name] = [off_xy, pos, off_o]
      for d_name, d_xy in def_dict.items():
        distance = 100
        name_o = ''
        receiver_o = 0
        for o_name, o_xy in off_dict.items():
          o_dist = dist(d_xy[0], o_xy[0])
          if o_dist < distance:
            distance = o_dist
            name_o = o_name
            receiver_o = o_xy[2]
        data.append([gameid, y, d_name, d_xy[1], distance, d_xy[0][0], d_xy[0][1], d_xy[2], name_o, receiver_o, down_distance[0][0], down_distance[0][1]])
      football = week.loc[(week['event'] == 'ball_snap') & (week['gameId'] == gameid) & (week['playId'] == y) & (week['displayName'] == 'Football'),['x', 'y', 'position', 'displayName', 'o']].values
      try:
        data.append([gameid, y, football[0][3], 'N/A', 'N/A', football[0][0], football[0][1], 'N/A', 'N/A', 'N/A'])
      except:
        football = week.loc[(week['event'] == 'None') & (week['gameId'] == gameid) & (week['playId'] == y) & (week['displayName'] == 'Football'),['x', 'y', 'position', 'displayName', 'o']].values
        data.append([gameid, y, football[0][3], 'N/A', 'N/A', football[0][0], football[0][1], 'N/A', 'N/A', 'N/A'])
    output = pd.DataFrame(data, columns = ['gameId', 'playId', 'displayName', 'position', 'dist_to_receiver', 'd_x', 'd_y', 'defender_o', 'receiver_displayName', 'receiver_o', 'down', 'distance'])
    return output

#Function to apply coverage to data
def coverage_labeler(data, week):
  lst_gameids = data.gameId.unique()
  lst_df = []
  for x in lst_gameids:
    lst_playids = data[data['gameId'] == x].playId.unique()
    df1 = Defender_dist(data, x, lst_playids)
    temp = coverage2(df1, week)
    #print(temp)
    #temp['gameId'] = x
    #temp['coverage'] = temp.apply(coverage_creator, axis = 1)
    lst_df.append(temp)
    #df2.append(temp) #need to some how get the temp dataframe into a list and then make a new df from the list of lists
  df3 = pd.concat(lst_df)
  df3['coverage'] = df3.apply(coverage_creator, axis = 1)
  #coverage = df3['coverage']
  #plays_mod = plays.join(coverage)
  plays_mod = pd.merge(plays, df3.loc[:, ['index', 'gameID', 'coverage']], how = 'right', left_on = ['playId', 'gameId'], right_on = ['index', 'gameID']).drop(['gameID', 'index'], axis = 1)
  return plays_mod


#returns wheter a play had trips or not
def Trips_detector(week):
  gameid_lst = week.gameId.unique()
  data = []
  for x in gameid_lst:
    playid_lst = week[week['gameId'] == x].playId.unique()
    for y in playid_lst:
      #get x/y coordinates of qb and football to determine which way the offense is going
      Football = week.loc[(week['event'] == 'ball_snap') & (week['gameId'] == x) & (week['playId'] == y) & (week['displayName'] == 'Football'),['x', 'y']].values
      QB = week.loc[(week['event'] == 'ball_snap') & (week['gameId'] == x) & (week['playId'] == y) & (week['position'] == 'QB'),['x', 'y']].values
      Receivers = week.loc[(week['event'] == 'ball_snap') & (week['gameId'] == x) & (week['playId'] == y) & ((week['position'] == 'WR') | (week['position'] == 'TE')),['x', 'y']].values
      right = 0
      left = 0
      if QB.shape[0] == 0:
        continue
      if Football.shape[0] == 0:
        Football = week.loc[(week['event'] == 'None') & (week['gameId'] == x) & (week['playId'] == y) & (week['displayName'] == 'Football'),['x', 'y']].values
        #QB = week.loc[(week['event'] == 'ball_snap') & (week['gameId'] == x) & (week['playId'] == y) & (week['position'] == 'P'),['x', 'y']].values
      if QB[0][0] > Football[0][0]:
        for z in Receivers:
          if z[1] >Football[0][1]:
            right += 1
          else:
            left += 1
      else:
        for z in Receivers:
          if z[1] < Football[0][1]:
            right += 1
          else:
            left += 1
      if right > 2:
        data.append([x, y, 'Yes', 'Right'])
      elif left > 2:
        data.append([x, y, 'Yes', 'Left'])
      else:
        data.append([x, y, 'No', np.nan])
  output = pd.DataFrame(data, columns = ['gameId', 'playId', 'Trips', 'Trips_Side'])
  return output

#basic function to perform joins on two dataframes
def plays_joiner(data1, data2):
  plays_mod = pd.merge(data1, data2, how = 'left', left_on = ['playId', 'gameId'], right_on = ['playId', 'gameId'])#.drop(['gameId'], axis = 1)
  return plays_mod

#Determines all the routes run on a play by the receivers from left to right, MID designates the middle of the field
def route_combos(week):
  gameid_lst = week.gameId.unique()
  data = []
  for x in gameid_lst:
    playid_lst = week[week['gameId'] == x].playId.unique()
    for y in playid_lst:
      #get x/y coordinates of qb and football to determine which way the offense is going
      Football = week.loc[(week['event'] == 'ball_snap') & (week['gameId'] == x) & (week['playId'] == y) & (week['displayName'] == 'Football'),['x', 'y']].values
      QB = week.loc[(week['event'] == 'ball_snap') & (week['gameId'] == x) & (week['playId'] == y) & (week['position'] == 'QB'),['x', 'y']].values
      Receivers = week.loc[(week['event'] == 'ball_snap') & (week['gameId'] == x) & (week['playId'] == y) & ((week['position'] == 'WR') | (week['position'] == 'TE')),['x', 'y', 'route']].sort_values(by = 'y').values
      if QB.shape[0] == 0:
        continue
      if Football.shape[0] == 0:
        Football = week.loc[(week['event'] == 'None') & (week['gameId'] == x) & (week['playId'] == y) & (week['displayName'] == 'Football'),['x', 'y']].values
        #QB = week.loc[(week['event'] == 'ball_snap') & (week['gameId'] == x) & (week['playId'] == y) & (week['position'] == 'P'),['x', 'y']].values
      if QB[0][0] > Football[0][0]:
        #going left, higher y is right
        Receivers = week.loc[(week['event'] == 'ball_snap') & (week['gameId'] == x) & (week['playId'] == y) & ((week['position'] == 'WR') | (week['position'] == 'TE')),['x', 'y', 'route']].sort_values(by = 'y', ascending = True).values
        left_routes = ''
        right_routes = ''
        for z in Receivers:
          if (z[1] < Football[0][1]) and (not (z[2] is np.nan)):
            left_routes += z[2] + ':'
          elif (z[1] > Football[0][1]) and (not (z[2] is np.nan)):
            right_routes += z[2] + ':'
      else:
        Receivers = week.loc[(week['event'] == 'ball_snap') & (week['gameId'] == x) & (week['playId'] == y) & ((week['position'] == 'WR') | (week['position'] == 'TE')),['x', 'y', 'route']].sort_values(by = 'y', ascending = False).values
        left_routes = ''
        right_routes = ''
        for z in Receivers:
          if (z[1] > Football[0][1]) and (not (z[2] is np.nan)):
            left_routes += z[2] + ':'
          elif (z[1] < Football[0][1]) and (not (z[2] is np.nan)):
            right_routes += z[2] + ':'
      routes = left_routes[0:-1] + '|MID|' + right_routes[0:-1]
      data.append([x, y, routes])
  output = pd.DataFrame(data, columns = ['gameId', 'playId', 'Routes'])
  return output

#Coverage logic for applying determining which plays are in what type of coverage
def coverage2(data, week):
  """

  Parameters:
    -data: Dataframe object
  Returns:
    New Dataframe with coverage for each play
  """

  playNums = data.playId.unique()
  coverages = {}
  games = []
  for play in playNums:
    coverages[play] = {}  
    df = data.copy()
    df = distance_from_ball(df,play)
    defenders = ['CB','FS','SS','DB','MLB','OLB','ILB','LB','S']
    df = df[df.position.isin(defenders)].query('displayName != "Football" and playId == @play')
    for index,row in df.iterrows():
      x = row.distance_from_ball_x
      y = row.distance_from_ball_y
      try:
        ball_o = week.query('position == "QB" and event == "ball_snap" and playId == @play').o.values[0]
      except:
        continue
      game = row.gameId
      #setting different zone drops for various distance for first down
      if row.distance > 15: #deep drops
        db_depth_c2 = 25
        db_depth_c3 = 16
      else: #shallow drops
        db_depth_c2 = 18
        db_depth_c3 = 10
      #determining man vs zone coverage by player orientation 
      if row.defender_o > 330 and row.receiver_o < 30: #standardizing by degrees
        row.defender = row.defender_o - 360
      elif row.defender_o < 30 and row.receiver_o > 330:
        row.offense_o = row.receiver_o - 360
      if abs(row.defender_o - row.receiver_o) < 30 and row.dist_to_receiver <=2: 
         #man coverage
        if 'man_to_man' in coverages[play]:
          coverages[play]['man_to_man'] += 1
        else:
          coverages[play]['man_to_man'] = 1
      #zone coverage
      else:
        if x >= db_depth_c2 and y >= 6 and 170 < abs(row.defender_o - ball_o) < 190: #deep and not in the middle of the ball
          if 'deep_half' in coverages[play]:
            coverages[play]['deep_half'] += 1
          else:
            coverages[play]['deep_half'] = 1
        elif x > db_depth_c3:
          if 0 < y < 6:
            if 'middle_third' in coverages[play]:
              coverages[play]['middle_third'] += 1
            else:
              coverages[play]['middle_third'] = 1
          else:
            if 'outside_third' in coverages[play]:
              coverages[play]['outside_third'] += 1
            else:
              coverages[play]['outside_third'] = 1
        elif row.distance_from_ball_x <= 3 and row.distance_from_ball_y <= 3:
            if 'blitzer' in coverages[play]:
              coverages[play]['blitzer'] += 1
            else:
              coverages[play]['blitzer'] = 1
        elif 170 < abs(row.defender_o - ball_o) < 190: #defenders facing the ball
            if 'hook_flat_zone' in coverages[play]:
              coverages[play]['hook_flat_zone'] += 1
            else:
                coverages[play]['hook_flat_zone'] = 1 
        games.append(game)

  columns=['deep_half','middle_third','outside_third','hook_flat_zone','man_to_man','blitzer']
  newdf = pd.DataFrame(coverages)
  newdf = newdf.transpose()
  newdf.reset_index(inplace=True)
  newdf['gameID'] = pd.Series(games)
  newdf.fillna(0, inplace = True)
  #newdf.columns = ['playId','hook_flat_zone','middle_third','match_zone','man_to_man','deep_half','outside_third','gameID']  
  return newdf

#runs through data created with coverage 2 and determines which coverage the defense is in
def coverage_creator(row):
  if row.man_to_man >= 2: #two players in man coverage
    if row.deep_half >= 1:
      return 'cover 2 man'
    if row.middle_third == 1:
      return 'cover 1 man'
    if row.middle_third + row.deep_half == 0:
      return 'cover 0' 
    else:
      return 'match coverage'
  else:
    if row.middle_third == 1 or  row.outside_third >= 1 :
      return  'cover 3'
    elif row.deep_half >= 1:
      return 'cover 2'
    else:
      return 'match coverage'

#adds which team is on offense to a dataframe.
def offense(df):
  lst = []
  for index, row in df.iterrows():
    playNum = row.playId
    game = row.gameId
    posteam = plays.query('playId == @playNum and gameId == @game').possessionTeam.values[0]
    lst.append(posteam)
  df['offense'] = lst
  return df

#adds which team is on defense to a dataframe
def defense(df):
  lst = []
  for index, row in df.iterrows():
    playNum = row.playId
    game = row.gameId
    offense = row.offense
    #print(offense)
    www = games.loc[(games['gameId'] == game), ['homeTeamAbbr','visitorTeamAbbr']].values[0]
    if offense not in www[0]:
      defense = www[0]
    if offense not in www[1]:
      defense = www[1]
    lst.append(defense)
  df['defense'] = lst
  return df

#finds the distance from the ball
def distance_from_ball(data,playNum):
  df = data.query('playId == @playNum')
  df = df.assign(distance_from_ball_x = abs(df.d_x - df.query('displayName == "Football"').d_x.values), distance_from_ball_y = abs(df.d_y - df.query('displayName == "Football"').d_y.values))
  return df



#runs through all weeks and makes the updated plays files for each week
dfs = [week1, week2, week3, week4, week5, week6, week7, week8, week9, week10, week11, week12, week13, week14, week15, week16, week17]

week1_test = week1.loc[(week1['gameId'] == 2018090600) | (week1['gameId'] == 2018090907)]
number = 1
for csv in dfs:
    print(number)
    result_cov = coverage_labeler(csv, csv)
    print('coverage done')
    result_trips = Trips_detector(csv)
    print('trips done')
    result_2 = plays_joiner(result_cov, result_trips)
    result_1 = route_combos(csv)
    print('route combo done')
    result_3 = plays_joiner(result_2, result_1)
    result_4 = offense(result_3)
    result_final = defense(result_4)
    str_name = 'week' + str(number)+ '_plays.csv'
    result_final.to_csv(str_name)
    print('week {} is done'.format(number))
    number += 1
