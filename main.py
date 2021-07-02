import pygame

pygame.init()

screen_width = 960
screen_height = 540

COLOR_INACTIVE = (0, 0, 0)
COLOR_ACTIVE = pygame.Color("limegreen")

course_info = {"Brae":       [3, 7, 17, 1, 13, 9, 15, 11, 5, 4, 10, 2, 18, 8, 16, 6, 14, 12, 
                              4, 4, 3, 5, 4, 5, 3, 4, 4, 5, 4, 4, 3, 4, 3, 5, 3, 5], 
               "Crag":       [5, 7, 17, 3, 9, 13, 11, 15, 1, 2, 10, 14, 18, 16, 12, 8, 6, 4, 
                              5, 4, 3, 4, 4, 4, 5, 3, 4, 5, 4, 3, 4, 3, 4, 4, 4, 5], 
               "Dorchester": [1, 9, 15, 7, 3, 11, 13, 17, 5, 8, 18, 10, 14, 2, 4, 16, 12, 6, 
                              4, 4, 3, 4, 5, 4, 4, 3, 5, 4, 4, 5, 3, 5, 4, 4, 3, 4], 
               "Stonehenge": [5, 7, 17, 1, 15, 13, 11, 3, 9, 8, 16, 6, 10, 18, 2, 14, 12, 4, 
                              4, 5, 3, 4, 3, 4, 4, 5, 4, 5, 3, 4, 4, 3, 5, 4, 4, 4], 
               "Tansi":      [1, 15, 13, 17, 5, 7, 11, 9, 3, 6, 18, 16, 8, 10, 14, 12, 4, 2, 
                              4, 4, 3, 4, 5, 3, 4, 4, 5, 4, 4, 3, 4, 5, 3, 4, 4, 5], 
               "Druid":      [17, 9, 15, 11, 3, 7, 1, 13, 5, 16, 8, 4, 10, 2, 18, 14, 6, 12, 
                              4, 5, 4, 3, 4, 4, 5, 3, 4, 4, 4, 4, 3, 5, 3, 4, 4, 5]}

def IndividualQuota():

  global quota, course_handicaps
  quota = {}

  for player in players:
    quota[player] = players[player]["Handicap"]

  for i in range(1, 19):
    for player in players:
      score = players[player]["Hole " + str(i)]
      
      if score - course_handicaps[i+17] == -2:
        hole_quota = 8
      elif score - course_handicaps[i+17] == -1:
        hole_quota = 4
      elif score == course_handicaps[i+17]:
        hole_quota = 2
      elif score - course_handicaps[i+17] == 1:
        hole_quota = 1
      elif score - course_handicaps[i+17] >= 2:
        hole_quota = 0
      else:
        print('Something is wrong with this quota calculation')

      quota[player] += hole_quota
  
  global results
  results["Individual Quota"] = quota
  print(quota)

def IndividualSkins():
        
  global skins
  skins = {}

  for i in range(1, 19):
    lowscore = []
    duplicate = False

    for player in players:
      if len(lowscore) == 0: # if lowscore for that hole does not exist, add first player
        lowscore = [player, players[player]["Hole " + str(i) + " Net"]]
        duplicate = False
      elif players[player]["Hole " + str(i) + " Net"] < lowscore[1]: # if current player's score is less than current low, replace the low score
        lowscore = [player, players[player]["Hole " + str(i) + " Net"]]
        duplicate = False
      elif players[player]["Hole " + str(i) + " Net"] == lowscore[1]: # if the current player's score equals the current low, set a flag that there should be no skin on that hole
        duplicate = True

    if duplicate == False: # if there is no duplicate and there is a skin, add the name and hole to a list
      skins[i] = lowscore[0]

  global results
  results["Individual Skins"] = skins
  print(skins)

def TeamPoints():
  global teams, team_points

  # Key: Ace 20, Eagle 10, Birdie 5, Par 3, Bogey 1, Double -1, Other -2

  team_points = {}
  for team in teams:

    team_points[team] = 0

    for player in teams[team]:

      for k in range(0, 18):
          
        score = players[player]["Hole " + str(k+1) + " Net"]

        if score - course_handicaps[k+18] == -2 and course_handicaps[k+1] == 3:
          points = 20
        elif score - course_handicaps[k+18] == -2:
          points = 10
        elif score - course_handicaps[k+18] == -1:
          points = 5
        elif score - course_handicaps[k+18] == 0:
          points = 3
        elif score - course_handicaps[k+18] == 1:
          points = 1
        elif score - course_handicaps[k+18] == 2:
          points = -1
        else:
          points = -2

        team_points[team] += points

  global results
  results["Team Points"] = team_points
  print(team_points)

def Shamble():

  global teams, shambleScores

  scores = {}
  shambleScores = {}
  for team in teams:

    shambleScores[team] = 0
    scores[team] = {}

    for k in range(0, 18):

      if k < 9:
        j = 0

        for player in teams[team]:
          score = players[player]["Hole " + str(k+1) + " Net"]

          if j == 0:
            prev_score = score
          elif j == 1:
            if score < prev_score:
              prev_score = score
            elif score >= prev_score:
              pass
            else:
              print("Issue with Shamble game")
          
          j += 1
        
        scores[team]["Hole " + str(k+1)] = prev_score
      
      else:
        total_score = 0
        for player in teams[team]:
          total_score += players[player]["Hole " + str(k+1) + " Net"]
        
        scores[team]["Hole " + str(k+1)] = total_score
  
  for i in range(1, 19):

    lowscore = 100
    for team in teams:
      if scores[team]["Hole " + str(i)] < lowscore:
        lowscore = scores[team]["Hole " + str(i)]
    
    for team in teams:
      if scores[team]["Hole " + str(i)] == lowscore:
        print(i, lowscore)
        shambleScores[team] += 1
  
  global results
  results["Shamble"] = shambleScores
  print(shambleScores)

def TeamSkins():

  global teams
  team_skins = {}
  last_skin = 0
  for i in range(1, 19):
    player_low = []
    lowscore = []

    for player in players:
      if len(lowscore) == 0: # if lowscore for that hole does not exist, add first player
        lowscore = [player, players[player]["Hole " + str(i) + " Net"]]
        player_low = [player]

      elif players[player]["Hole " + str(i) + " Net"] < lowscore[1]: # if current player's score is less than current low, replace the low score
        lowscore = [player, players[player]["Hole " + str(i) + " Net"]]
        player_low = [player]

      elif players[player]["Hole " + str(i) + " Net"] == lowscore[1]: # if the current player's score equals the current low, set a flag that there should be no skin on that hole
        player_low.append(player)

    if len(player_low) == 1: # if there is no duplicate and there is a skin, add the name and hole to a list
      for team in teams:
        if player_low[0] in teams[team]:
          if team in team_skins:
            team_skins[team] += i - last_skin
            last_skin = i
            print(team, i, lowscore[1])
          else:
            team_skins[team] = i - last_skin
            last_skin = i
            print(team, i, lowscore[1])
    else:
      if len(player_low) >= 3:
        pass
      elif len(player_low) == 2:
        for team in teams:
          if player_low[0] in teams[team] and player_low[1] in teams[team]:
            if team in team_skins:
              team_skins[team] += i - last_skin
              last_skin = i
            else:
              team_skins[team] = i - last_skin
              last_skin = i
              print(team, i, lowscore[1])
          else:
            pass

  scores = {}
  for team in teams:

    scores[team] = {}

    if team not in team_skins:
      team_skins[team] = 0

    for k in range(0, 18):
      total_score = 0

      for player in teams[team]:
        total_score += players[player]["Hole " + str(k+1) + " Net"]

      scores[team]["Hole " + str(k+1)] = total_score
  
  last_skin = 0
  for i in range(0, 18):
    lowscore = []
    duplicate = False

    for team in teams:

      if len(lowscore) == 0:
        lowscore = [team, scores[team]["Hole " + str(i+1)]]
        duplicate = False
      elif int(scores[team]["Hole " + str(i+1)]) < int(lowscore[1]):
        lowscore = [team, scores[team]["Hole " + str(i+1)]]
        duplicate = False
      elif int(scores[team]["Hole " + str(i+1)]) == int(lowscore[1]):
        duplicate = True

    if duplicate == False:
      team_skins[lowscore[0]] += i+1-last_skin
      last_skin = i+1
      print(team, i+1, lowscore[1])
  
  global results
  results["Team Skins"] = team_skins
  print(team_skins)

def TeamQuotaSkins():

  ###############################################################
  # ADD NET SCORE AS THE GAME FOR THIS DAY
  # SPLIT MONEY WITH TEAMMATE FOR TEAM QUOTA AND TEAM SKINSN

  # These games print only one of the player's names per team

  global teams

  teamQuota = {}
  for team in teams:
    teamQuota[team] = 0

    for player in teams[team]:
      teamQuota[team] += players[player]["Handicap"]

    #teamQuota[team] = teamQuota[team] / 2
  
  quotas = {}
  for team in teams:
    i = 1
    
    for player in teams[team]:
        
      if i != 1:
        del players[player]
        break
      
      players[player]["Handicap"] = teamQuota[team]
      quotas[player] = teamQuota[team]
      i += 1

  for i in range(1, 19):

    count = 1
    for player in players:

      score = players[player]["Hole " + str(i)]
      
      if score - course_handicaps[i+17] == -2:
        hole_quota = 8
      elif score - course_handicaps[i+17] == -1:
        hole_quota = 4
      elif score == course_handicaps[i+17]:
        hole_quota = 2
      elif score - course_handicaps[i+17] == 1:
        hole_quota = 1
      elif score - course_handicaps[i+17] >= 2:
        hole_quota = 0
      else:
        print('Something is wrong with this quota calculation')

      quotas[player] += hole_quota
      count += 1
  
  print("Team Quota: \n", quotas)

  # Re-calculate net scores
  
  for i in range(1, 19):

    for player in players:

      if course_handicaps[i-1] <= players[player]["Handicap"]:

        if players[player]["Handicap"] - course_handicaps[i-1] >= 18:
          players[player]["Hole " + str(i) + " Net"] = players[player]["Hole " + str(i)] - 2
        else:
          players[player]["Hole " + str(i) + " Net"] = players[player]["Hole " + str(i)] - 1
      else:
        players[player]["Hole " + str(i) + " Net"] = players[player]["Hole " + str(i)]

  skins = []
  for i in range(1, 19):
    lowscore = []
    duplicate = False

    for player in players:
      if len(lowscore) == 0: # if lowscore for that hole does not exist, add first player
        lowscore = [player, players[player]["Hole " + str(i) + " Net"]]
        duplicate = False
      elif players[player]["Hole " + str(i) + " Net"] < lowscore[1]: # if current player's score is less than current low, replace the low score
        lowscore = [player, players[player]["Hole " + str(i) + " Net"]]
        duplicate = False
      elif players[player]["Hole " + str(i) + " Net"] == lowscore[1]: # if the current player's score equals the current low, set a flag that there should be no skin on that hole
        duplicate = True

    if duplicate == False: # if there is no duplicate and there is a skin, add the name and hole to a list
      skins.append([lowscore[0], i])

  print("Here are the results for team skins:\n", skins)

# FIX THIS
def TeamPlacePoints():

  global teams

  # Combined score each hole, 1=6, 2=4, 3=2, 4=0, if tied, split
  scores = {}
  teamPlacePointsResults = {}
  for team in teams:
    scores[team] = {}
    teamPlacePointsResults[team] = 0
    for i in range(1, 19):
      scores[team]["Hole " + str(i)] = 0
      for player in teams[team]:
        scores[team]["Hole " + str(i)] += players[player]["Hole " + str(i) + " Net"]

  teamPlacePoints = {}
  countFirst = {}
  countSecond = {}
  countThird = {}
  first = 6
  second = 4
  third = 2
  fourth = 0
  fifth = 2
  sixth = 0
  for i in range(1, 19):
    teamPlacePoints[i] = []

    for team in teams:
      teamPlacePoints[i].append([team, scores[team]["Hole " + str(i)]])
    
    teamPlacePoints[i].sort(key=lambda x: x[1])
    countFirst[i] = sum(x.count(teamPlacePoints[i][0][1]) for x in teamPlacePoints[i])
    if countFirst[i] == 1:
      teamPlacePointsResults[teamPlacePoints[i][0][0]] += first
      countSecond[i] = sum(x.count(teamPlacePoints[i][1][1]) for x in teamPlacePoints[i])
      if countSecond[i] == 1:
        teamPlacePointsResults[teamPlacePoints[i][1][0]] += second
        countThird[i] = sum(x.count(teamPlacePoints[i][2][1]) for x in teamPlacePoints[i])
        if countThird[i] == 1:
          teamPlacePointsResults[teamPlacePoints[i][2][0]] += third
          teamPlacePointsResults[teamPlacePoints[i][3][0]] += fourth
        else:
          teamPlacePointsResults[teamPlacePoints[i][2][0]] += (third+fourth)/2
          teamPlacePointsResults[teamPlacePoints[i][3][0]] += (third+fourth)/2
      elif countSecond[i] == 2:
        teamPlacePointsResults[teamPlacePoints[i][1][0]] += (second+third)/2
        teamPlacePointsResults[teamPlacePoints[i][2][0]] += (second+third)/2
        teamPlacePointsResults[teamPlacePoints[i][3][0]] += fourth
      elif countSecond[i] == 3:
        teamPlacePointsResults[teamPlacePoints[i][1][0]] += (second+third+fourth)/3
        teamPlacePointsResults[teamPlacePoints[i][2][0]] += (second+third+fourth)/3
        teamPlacePointsResults[teamPlacePoints[i][3][0]] += (second+third+fourth)/3
    
    elif countFirst[i] == 2:
      teamPlacePointsResults[teamPlacePoints[i][0][0]] += (first+second)/2
      teamPlacePointsResults[teamPlacePoints[i][1][0]] += (first+second)/2
      countThird[i] = sum(x.count(teamPlacePoints[i][2][1]) for x in teamPlacePoints[i])
      if countThird[i] == 1:
        teamPlacePointsResults[teamPlacePoints[i][2][0]] += third
        teamPlacePointsResults[teamPlacePoints[i][3][0]] += fourth
      else:
        teamPlacePointsResults[teamPlacePoints[i][2][0]] += (third+fourth)/2
        teamPlacePointsResults[teamPlacePoints[i][3][0]] += (third+fourth)/2
    
    elif countFirst[i] == 3:
      teamPlacePointsResults[teamPlacePoints[i][0][0]] += (first+second+third)/3
      teamPlacePointsResults[teamPlacePoints[i][1][0]] += (first+second+third)/3
      teamPlacePointsResults[teamPlacePoints[i][2][0]] += (first+second+third)/3
      teamPlacePointsResults[teamPlacePoints[i][3][0]] += fourth
    
    elif countFirst[i] == 4:
      teamPlacePointsResults[teamPlacePoints[i][0][0]] += (first+second+third+fourth)/4
      teamPlacePointsResults[teamPlacePoints[i][1][0]] += (first+second+third+fourth)/4
      teamPlacePointsResults[teamPlacePoints[i][2][0]] += (first+second+third+fourth)/4
      teamPlacePointsResults[teamPlacePoints[i][3][0]] += (first+second+third+fourth)/4
  
  print(teams)
  print(teamPlacePointsResults)

def Vegas():

  global teams

  vegas = {}
  for team in teams:
    vegas[team] = 0
    for i in range(1, 19):
      scores = []
      for player in teams[team]:
        scores.append(players[player]["Hole " + str(i) + " Net"])
      
      scores.sort()
      string = ""
      for score in scores:
        string = string + str(score)
      
      vegasScore = int(string)
      vegas[team] += vegasScore
  
  print(vegas)

class InputBox:
  
  def __init__(self, x, y, w, h, font_size, text=""):
    self.rect = pygame.Rect(x, y, w, h)
    self.color = COLOR_INACTIVE
    self.text = text
    self.font = pygame.font.Font(None, font_size)
    self.txt_surface = self.font.render(text, True, self.color)
    self.active = False
  
  def handle_event(self, event):

    pointer = pygame.mouse.get_pos()
    if self.rect.collidepoint(pointer):
      self.active = True
    else:
      self.active = False
    
    self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE

    """
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        self.active = not self.active
      else:
        self.active = False
      self.color = COLOR_ACTIVE if self.active else COLOR_INACTIVE
      """

    if event.type == pygame.KEYDOWN:
      if self.active:
        if event.key == pygame.K_RETURN:
          print(self.text)
        elif event.key == pygame.K_BACKSPACE:
          self.text = self.text[:-1]
        else:
          self.text += event.unicode
        self.txt_surface = self.font.render(self.text, True, self.color)

  def update(self):
    # Resize if too long
    width = max(self.txt_surface.get_width(), self.rect.w)
    self.rect.w = width
  
  def draw(self, screen):
    text_rect = self.txt_surface.get_rect(center=self.rect.center)
    screen.blit(self.txt_surface, text_rect)
    pygame.draw.rect(screen, self.color, self.rect, 2)


class CourseBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        #global active_scene
        global course_handicaps, course_name
        course_handicaps = course_info[self.text]
        course_name = self.text

        active_scene.next = ScoreCardScene()


class NextScorecardBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):

        active_scene.ExtractInfo()

        active_scene.next = ScoreCardScene()


class IndividualQuotaGameBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        IndividualQuota()


class IndividualSkinsGameBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        IndividualSkins()


class TeamPointsGameBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        TeamPoints()


class ShambleGameBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        Shamble()


class TeamSkinsGameBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        TeamSkins()


class TeamQuotaSkinsGameBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        TeamQuotaSkins()


class TeamPlacePointsGameBox(InputBox):
  
  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        TeamPlacePoints()


class VegasGameBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        Vegas()


class CalculateResultsBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        active_scene.next = ResultsScene()


class DisplayIndividualQuotaBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        active_scene.next = IndividualQuotaScene()


class DisplayIndividualSkinsBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        active_scene.next = IndividualSkinsScene()


class DisplayTeamPointsBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        active_scene.next = TeamPointsScene()


class DisplayShambleBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        active_scene.next = ShambleScene()


class DisplayTeamSkinsBox(InputBox):

  def __init__(self, x, y, w, h, font_size, text=""):
    super().__init__(x, y, w, h, font_size, text)
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        active_scene.next = TeamSkinsScene()


class QuitBox:
  
  def __init__(self, x, y, w, h, font_size, text="Quit"):
    self.rect = pygame.Rect(x, y, w, h)
    self.color = COLOR_INACTIVE
    self.text = text
    self.font = pygame.font.Font(None, font_size)
    self.txt_surface = self.font.render(text, True, self.color)
    self.active = False
  
  def handle_event(self, event):
    if event.type == pygame.MOUSEBUTTONDOWN:
      if self.rect.collidepoint(event.pos):
        return True
      else:
        return False
  
  def draw(self, screen):
    text_rect = self.txt_surface.get_rect(center=self.rect.center)
    screen.blit(self.txt_surface, text_rect)
    pygame.draw.rect(screen, self.color, self.rect, 2)


class SceneBase:

  def __init__(self):
    self.next = self
    
  def ProcessInput(self, events, pressed_keys):
    print("uh-oh, you didn't override this in the child class")

  def Update(self):
    print("uh-oh, you didn't override this in the child class")

  def Render(self, screen):
    print("uh-oh, you didn't override this in the child class")

  def SwitchToScene(self, next_scene):
    self.next = next_scene
    
  def Terminate(self):
    self.SwitchToScene(None)


class TitleScene(SceneBase):

  def __init__(self):
    super().__init__()

    # Box that displays title of scene
    self.title_box = InputBox(0, 0, screen_width, screen_height//4, int(screen_height//4), text="Select Course")

    # Boxes for all the courses
    self.brae = CourseBox(0, screen_height//4, screen_width//2, screen_height//4, int(screen_height//5), text="Brae")

    self.crag = CourseBox(screen_width//2, screen_height//4, screen_width//2, screen_height//4, int(screen_height//5), text="Crag")

    self.dorchester = CourseBox(0, 2*screen_height//4, screen_width//2, screen_height//4, int(screen_height//5), text="Dorchester")

    self.stonehenge = CourseBox(screen_width//2, 2*screen_height//4, screen_width//2, screen_height//4, int(screen_height//5), text="Stonehenge")

    self.tansi = CourseBox(0, 3*screen_height//4, screen_width//2, screen_height//4, int(screen_height//5), text="Tansi")

    self.druid = CourseBox(screen_width//2, 3*screen_height//4, screen_width//2, screen_height//4, int(screen_height//5), text="Druid")

    # Combine all boxes to render at once
    self.boxes = [self.title_box, self.brae, self.crag, self.dorchester, self.stonehenge, self.tansi, self.druid]

  def ProcessInput(self, events, pressed_keys):
    for event in events:
      for box in self.boxes:
        box.handle_event(event)

  def Update(self):
    for box in self.boxes:
      box.update()
  
  def Render(self, screen):
    screen.fill((255, 255, 255))
    for box in self.boxes:
      box.draw(screen)


class ScoreCardScene(SceneBase):

  def __init__(self):
    super().__init__()

    global course_name
    # Box for displaying course name
    self.course_title_box = InputBox(0, 0, screen_width, screen_height/9*2, int(screen_height/9*2), text=course_name)

    # Labels for holes
    self.hole_input = InputBox(0, screen_height//9*2, screen_width//10, screen_height//9, int(screen_height//18), text="HOLE")

    # Boxes for hole score
    self.scores = []
    hole = 1
    for i in range(19):
      if i != 18:
        self.scores.append(InputBox(screen_width//10+i*0.9*screen_width//19, screen_height//9*2, (9*screen_width/10//19), screen_height//9, int(screen_height//19), text=str(hole)))
        hole += 1

      elif i == 18:
        self.scores.append(InputBox(screen_width//10+i*0.9*screen_width//19, screen_height//9*2, (9*screen_width/10//19), screen_height//9, int(screen_height//19), text="H"))

    # Labels for handicaps
    self.handicap_input = InputBox(0, screen_height//9*3, screen_width//10, screen_height//9, int(screen_height//19), text="HDCP")

    # Test boxes for hole score
    self.handicaps = []
    hole = 1
    for i in range(19):
      if i != 18:
        self.handicaps.append(InputBox(screen_width//10+i*0.9*screen_width//19, screen_height//9*3, (9*screen_width/10//19), screen_height//9, int(screen_height//19), text=str(course_handicaps[hole-1])))
        hole += 1
      elif i == 18:
        self.handicaps.append(InputBox(screen_width//10+i*0.9*screen_width//19, screen_height//9*3, (9*screen_width/10//19), screen_height//9, int(screen_height//19)))

    # Test boxes for player inputs
    self.players = {}
    for j in range(4):
      self.players[j] = [InputBox(0, screen_height//9*(4+j), screen_width//10, screen_height//9, int(screen_height//19))]
      for i in range(19):
        self.players[j].append(InputBox(screen_width//10+i*0.9*screen_width//19, screen_height//9*(4+j), (9*screen_width/10//19), screen_height/9, int(screen_height/19)))

    # Next box for another scorecard
    self.next_box = NextScorecardBox(screen_width-100, screen_height-20, 50, 20, 15, text="Next")

    # Combine all text boxes
    self.boxes = [self.course_title_box, self.hole_input, self.handicap_input, self.next_box]
    for score in self.scores:
      self.boxes.append(score)
    for handicap in self.handicaps:
      self.boxes.append(handicap)
    for player in self.players:
      for input_box in self.players[player]:
        self.boxes.append(input_box)

    # Box to quit and extract scores
    self.quit = QuitBox(screen_width-50, screen_height-20, 50, 20, 15)

  def ProcessInput(self, events, pressed_keys):
    for event in events:
      for box in self.boxes:
        box.handle_event(event)
    
      if self.quit.handle_event(event):
        # Get player scores
        self.ExtractInfo()

        # Switch scene to select games
        self.SwitchToScene(GameSelectionScene())

        # Calculate and update net scores
        global players, course_handicaps
        for player in players:
          handicap = players[player]["Handicap"]

          for i in range(1, 19):
            if handicap - course_handicaps[i-1] >= 18:
              players[player]["Hole " + str(i) + " Net"] = players[player]["Hole " + str(i)] - 2
            elif handicap - course_handicaps[i-1] >= 0:
              players[player]["Hole " + str(i) + " Net"] = players[player]["Hole " + str(i)] - 1
            else:
              players[player]["Hole " + str(i) + " Net"] = players[player]["Hole " + str(i)]


  def Update(self):
    for box in self.boxes:
      box.update()
  
  def Render(self, screen):
    screen.fill((255, 255, 255))
    for box in self.boxes:
      box.draw(screen)
    
      self.quit.draw(screen)
  
  def ExtractInfo(self):
    global players, course_handicaps
    for player in self.players:
      i = 0
      hole = 1
      for box in self.players[player]:
        if i == 0:
          if box.text == "":
            continue
          else:
            players[box.text] = {}
            name = box.text
        elif i != 19:
          if box.text == "":
            hole += 1
          else:
            players[name]["Hole " + str(hole)] = int(box.text)
            hole += 1
        elif i == 19:
          players[name]["Handicap"] = int(box.text)
        
        i += 1

    global teams
    teams = {}
    i = 0
    j = 1
    for player in players:
      if i % 2 == 0:
        teams[j] = []
        teams[j].append(player)
        i += 1
      else:
        teams[j].append(player)
        j += 1
        i += 1


class GameSelectionScene(SceneBase):

  def __init__(self):
    super().__init__()

    # Box that displays title of scene
    self.title_box = InputBox(0, 0, screen_width, screen_height//6, int(screen_height//6), text="Select Games")

    # Box for individual quota
    self.individual_quota = IndividualQuotaGameBox(0, screen_height//6, screen_width//2, screen_height//6, int(screen_height//8), text="Individual Quota")

    # Box for individual skins
    self.individual_skins = IndividualSkinsGameBox(0, 2*screen_height//6, screen_width//2, screen_height//6, int(screen_height//8), text="Individual Skins")

    # Box for team points
    self.team_points = TeamPointsGameBox(0, 3*screen_height//6, screen_width//2, screen_height//6, int(screen_height//8), text="Team Points")

    # Box for shamble
    self.shamble = ShambleGameBox(screen_width//2, screen_height//6, screen_width//2, screen_height//6, int(screen_height//8), text="Shamble")

    # Box for team skins
    self.team_skins = TeamSkinsGameBox(screen_width//2, 2*screen_height//6, screen_width//2, screen_height//6, int(screen_height//8), text="Team Skins")

    # Box for team quota skins
    self.team_quota_skins = TeamQuotaSkinsGameBox(screen_width//2, 3*screen_height//6, screen_width//2, screen_height//6, int(screen_height//8), text="Team Quota/Skins")

    # Box for team place points
    self.team_place_points = TeamPlacePointsGameBox(0, 4*screen_height//6, screen_width//2, screen_height//6, int(screen_height//8), text="Team Place Points")

    # Box for vegas
    self.vegas = VegasGameBox(screen_width//2, 4*screen_height//6, screen_width//2, screen_height//6, int(screen_height//8), text="Vegas")

    # Box to go to results scene
    self.results = CalculateResultsBox(3*screen_width//8, 5*screen_height//6, screen_width//4, screen_height//6, int(screen_height//8), text="Results")

    # Combine boxes
    self.boxes = [self.title_box, self.individual_quota, self.individual_skins, self.team_points, self.shamble, self.team_skins, self.team_quota_skins, self.team_place_points, self.vegas, self.results]
  
  def ProcessInput(self, events, pressed_keys):
    for event in events:
      for box in self.boxes:
        box.handle_event(event)

  def Update(self):
    for box in self.boxes:
      box.update()
  
  def Render(self, screen):
    screen.fill((255, 255, 255))
    for box in self.boxes:
      box.draw(screen)


class ResultsScene(SceneBase):

  def __init__(self):
    super().__init__()

    global results

    # Box that displays title of scene
    self.title_box = InputBox(0, 0, screen_width, screen_height//6, int(screen_height//6), text="Select Result to Display")

    # Add boxes for each result in results dictionary
    self.results_boxes = []
    count = 0
    for result in results:
      if result == "Individual Quota":
        self.results_boxes.append(DisplayIndividualQuotaBox(screen_width//4, (count+2)*screen_height//6, screen_width//2, screen_height//6, int(screen_height//6), text="Individual Quota"))
        count += 1
      elif result == "Individual Skins":
        self.results_boxes.append(DisplayIndividualSkinsBox(screen_width//4, (count+2)*screen_height//6, screen_width//2, screen_height//6, int(screen_height//6), text="Individual Skins"))
        count += 1
      elif result == "Team Points":
        self.results_boxes.append(DisplayTeamPointsBox(screen_width//4, (count+2)*screen_height//6, screen_width//2, screen_height//6, int(screen_height//6), text="Team Points"))
        count += 1
      elif result == "Shamble":
        self.results_boxes.append(DisplayShambleBox(screen_width//4, (count+2)*screen_height//6, screen_width//2, screen_height//6, int(screen_height//6), text="Shamble"))
        count += 1
      elif result == "Team Skins":
        self.results_boxes.append(DisplayTeamSkinsBox(screen_width//4, (count+2)*screen_height//6, screen_width//2, screen_height//6, int(screen_height//6), text="Team Skins"))
        count += 1

    # Combine boxes
    self.boxes = [self.title_box]
    for box in self.results_boxes:
      self.boxes.append(box)
  
  
  def ProcessInput(self, events, pressed_keys):
    for event in events:
      for box in self.boxes:
        box.handle_event(event)

  def Update(self):
    for box in self.boxes:
      box.update()
  
  def Render(self, screen):
    screen.fill((255, 255, 255))
    for box in self.boxes:
      box.draw(screen)


class IndividualQuotaScene(SceneBase):

  def __init__(self):
    super().__init__()

    global results

    # Box that displays title of scene
    self.title_box = InputBox(0, 0, screen_width, screen_height//6, int(screen_height//6), text="Individual Quota")

    # Combine boxes
    self.boxes = [self.title_box]

    final_results = {k: v for k, v in sorted(results["Individual Quota"].items(), key=lambda item: item[1], reverse=True)}

    num = 1
    for player in final_results:
      if num < 7:
        place_label_text = str(num) + ": " + str(player) + " (" + str(final_results[player]) + ")"
        place_label = InputBox(0, screen_height//6+(num-1)*screen_height//8, screen_width//2, screen_height//8, int(screen_height//8), text=place_label_text)
        self.boxes.append(place_label)

        num += 1
      else:
        place_label_text = str(num) + ": " + str(player) + " (" + str(final_results[player]) + ")"
        place_label = InputBox(screen_width//2, screen_height//6+(num-7)*screen_height//8, screen_width//2, screen_height//8, int(screen_height//8), text=place_label_text)
        self.boxes.append(place_label)

        num += 1
  
  def ProcessInput(self, events, pressed_keys):
    for event in events:
      for box in self.boxes:
        box.handle_event(event)

  def Update(self):
    for box in self.boxes:
      box.update()
  
  def Render(self, screen):
    screen.fill((255, 255, 255))
    for box in self.boxes:
      box.draw(screen)


class IndividualSkinsScene(SceneBase):
  
  def __init__(self):
    super().__init__()

    global results

    # Box that displays title of scene
    self.title_box = InputBox(0, 0, screen_width, screen_height//6, int(screen_height//6), text="Individual Skins")

    # Combine boxes
    self.boxes = [self.title_box]

    # Determine skins results and carryovers
    skins_results = {}
    for player in players:
      skins_results[player] = 0
    last_skin = 0
    for skin_hole in results["Individual Skins"]:
      skins_results[results["Individual Skins"][skin_hole]] += (skin_hole - last_skin)
      last_skin = skin_hole
    
    # Make boxes for results
    skins_results = {k: v for k, v in sorted(skins_results.items(), key=lambda item: item[1], reverse=True)}
    num = 1
    for player in skins_results:
      if num < 7:
        place_label_text = str(num) + ": " + str(player) + " (" + str(skins_results[player]) + ")"
        place_label = InputBox(0, screen_height//6+(num-1)*screen_height//8, screen_width//2, screen_height//8, int(screen_height//8), text=place_label_text)
        self.boxes.append(place_label)

        num += 1
      else:
        place_label_text = str(num) + ": " + str(player) + " (" + str(skins_results[player]) + ")"
        place_label = InputBox(screen_width//2, screen_height//6+(num-7)*screen_height//8, screen_width//2, screen_height//8, int(screen_height//8), text=place_label_text)
        self.boxes.append(place_label)

        num += 1
  
  def ProcessInput(self, events, pressed_keys):
    for event in events:
      for box in self.boxes:
        box.handle_event(event)

  def Update(self):
    for box in self.boxes:
      box.update()
  
  def Render(self, screen):
    screen.fill((255, 255, 255))
    for box in self.boxes:
      box.draw(screen)


class TeamPointsScene(SceneBase):
  
  def __init__(self):
    super().__init__()

    global results

    # Box that displays title of scene
    self.title_box = InputBox(0, 0, screen_width, screen_height//6, int(screen_height//6), text="Team Points")

    # Combine boxes
    self.boxes = [self.title_box]
    
    # Make boxes for results
    results["Team Points"] = {k: v for k, v in sorted(results["Team Points"].items(), key=lambda item: item[1], reverse=True)}
    num = 1
    for team in results["Team Points"]:
      if num < 7:
        place_label_text = str(num) + ": " + str(teams[team][0]) + "/" + str(teams[team][1]) + " (" + str(results["Team Points"][team]) + ")"
        place_label = InputBox(0, screen_height//6+(num-1)*screen_height//8, screen_width//2, screen_height//8, int(screen_height//8), text=place_label_text)
        self.boxes.append(place_label)

        num += 1
      else:
        place_label_text = str(num) + ": " + str(teams[team][0]) + "/" + str(teams[team][1]) + " (" + str(results["Team Points"][team]) + ")"
        place_label = InputBox(screen_width//2, screen_height//6+(num-7)*screen_height//8, screen_width//2, screen_height//8, int(screen_height//8), text=place_label_text)
        self.boxes.append(place_label)

        num += 1
  
  def ProcessInput(self, events, pressed_keys):
    for event in events:
      for box in self.boxes:
        box.handle_event(event)

  def Update(self):
    for box in self.boxes:
      box.update()
  
  def Render(self, screen):
    screen.fill((255, 255, 255))
    for box in self.boxes:
      box.draw(screen)


class ShambleScene(SceneBase):

  def __init__(self):
    super().__init__()

    global results

    # Box that displays title of scene
    self.title_box = InputBox(0, 0, screen_width, screen_height//6, int(screen_height//6), text="Shamble")

    # Combine boxes
    self.boxes = [self.title_box]
    
    # Make boxes for results
    results["Shamble"] = {k: v for k, v in sorted(results["Shamble"].items(), key=lambda item: item[1], reverse=True)}
    num = 1
    for team in results["Shamble"]:
      if num < 7:
        place_label_text = str(num) + ": " + str(teams[team][0]) + "/" + str(teams[team][1]) + " (" + str(results["Shamble"][team]) + ")"
        place_label = InputBox(0, screen_height//6+(num-1)*screen_height//8, screen_width//2, screen_height//8, int(screen_height//8), text=place_label_text)
        self.boxes.append(place_label)

        num += 1
      else:
        place_label_text = str(num) + ": " + str(teams[team][0]) + "/" + str(teams[team][1]) + " (" + str(results["Shamble"][team]) + ")"
        place_label = InputBox(screen_width//2, screen_height//6+(num-7)*screen_height//8, screen_width//2, screen_height//8, int(screen_height//8), text=place_label_text)
        self.boxes.append(place_label)

        num += 1
  
  def ProcessInput(self, events, pressed_keys):
    for event in events:
      for box in self.boxes:
        box.handle_event(event)

  def Update(self):
    for box in self.boxes:
      box.update()
  
  def Render(self, screen):
    screen.fill((255, 255, 255))
    for box in self.boxes:
      box.draw(screen)


class TeamSkinsScene(SceneBase):
  
  def __init__(self):
    super().__init__()

    global results

    # Box that displays title of scene
    self.title_box = InputBox(0, 0, screen_width, screen_height//6, int(screen_height//6), text="Team Skins")

    # Combine boxes
    self.boxes = [self.title_box]
    
    # Make boxes for results
    results["Team Skins"] = {k: v for k, v in sorted(results["Team Skins"].items(), key=lambda item: item[1], reverse=True)}
    num = 1
    for team in results["Team Skins"]:
      if num < 7:
        place_label_text = str(num) + ": " + str(teams[team][0]) + "/" + str(teams[team][1]) + " (" + str(results["Team Skins"][team]) + ")"
        place_label = InputBox(0, screen_height//6+(num-1)*screen_height//8, screen_width//2, screen_height//8, int(screen_height//8), text=place_label_text)
        self.boxes.append(place_label)

        num += 1
      else:
        place_label_text = str(num) + ": " + str(teams[team][0]) + "/" + str(teams[team][1]) + " (" + str(results["Team Skins"][team]) + ")"
        place_label = InputBox(screen_width//2, screen_height//6+(num-7)*screen_height//8, screen_width//2, screen_height//8, int(screen_height//8), text=place_label_text)
        self.boxes.append(place_label)

        num += 1
  
  def ProcessInput(self, events, pressed_keys):
    for event in events:
      for box in self.boxes:
        box.handle_event(event)

  def Update(self):
    for box in self.boxes:
      box.update()
  
  def Render(self, screen):
    screen.fill((255, 255, 255))
    for box in self.boxes:
      box.draw(screen)


def run(width, height, fps, starting_scene):
  
  global active_scene, course_handicaps, players, results
  players = {}
  results = {}

  pygame.init()
  screen = pygame.display.set_mode((width, height))
  clock = pygame.time.Clock()

  active_scene = starting_scene

  while active_scene != None:
    pressed_keys = pygame.key.get_pressed()
    
    # Event filtering
    filtered_events = []
    for event in pygame.event.get():
      quit_attempt = False
      if event.type == pygame.QUIT:
        quit_attempt = True
      elif event.type == pygame.KEYDOWN:
        alt_pressed = pressed_keys[pygame.K_LALT] or \
                          pressed_keys[pygame.K_RALT]
        if event.key == pygame.K_ESCAPE:
          quit_attempt = True
        elif event.key == pygame.K_F4 and alt_pressed:
          quit_attempt = True
        
      if quit_attempt:
        active_scene.SwitchToScene(None)
      else:
        filtered_events.append(event)
    
    active_scene.ProcessInput(filtered_events, pressed_keys)
    active_scene.Update()
    active_scene.Render(screen)
    
    active_scene = active_scene.next
    
    pygame.display.flip()
    clock.tick(fps)

def main():

    run(screen_width, screen_height, 60, TitleScene())

if __name__ == "__main__":
  main()
  pygame.quit()

  print(teams)
