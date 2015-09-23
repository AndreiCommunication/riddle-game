from sys import exit
from time import sleep
from random import randint
from random import choice
import all_strings


class Engine(object):

    def __init__(self, a_map):
        self.map = a_map

    def play(self, start_room):
        # this will run for the duration of the game, using self.map to
        # navigate between the rooms

        next_room = self.map.play(start_room)

        while next_room != 'end':
            next_room = self.map.play(next_room)
        if next_room == 'end':
            self.map.play(next_room)


class Inventory(object):

    items = []
    failed_puzzles = 0

    def show(self):
        print "\nYour inventory:"
        for item in self.items:
            print item
        if not self.items:
            print all_strings.empty_inv

    def add(self, new_item):
        self.items.append(new_item)

    def add_to_top(self, new_item):
        self.items.insert(0, new_item)

    def remove(self, old_item):
        self.items.remove(old_item)

    def stones_carried(self):
        count = 0
        for item in self.items:
            if item.split()[0] == "Stone":
                count += 1
        return count

    def end_if_failed(self):
        if self.failed_puzzles >= 3:
            print all_strings.lose_game
            sleep(1.5)
            exit(1)


class Room(object):

    current_room = False
    guesses_left = 5
    solved = False
    stone_here = False
    visited = False
    bad_moves = []
    good_moves = []
    extra = ""
    helper = all_strings.helper
    bearings = all_strings.room_bearings

    def action(self):
        # basic action options for any room
        action = raw_input("> ").lower()
        while action not in self.good_moves:
            if action == 'touch stone' and 'take stone' in self.good_moves:
                print all_strings.touch_stone
            elif action in self.bad_moves:
                print all_strings.bad_moves
            elif action == "take":
                print all_strings.action_take
            elif action == "talk":
                print "\n%s\n" % choice(all_strings.talking)
            elif action == "go":
                print all_strings.action_go
            elif action == "walk":
                print all_strings.action_walk
            elif action == "touch":
                print all_strings.action_touch
            elif action == "sleep":
                print all_strings.action_sleep
            elif action == 'help':
                print all_strings.line_break
                print "\n" * 6
                print self.helper
            elif action == 'look around' or action == 'look':
                print all_strings.line_break
                print "\n" * 8
                print self.extra
                print self.bearings
            elif action == "intro":
                print all_strings.line_break
                print "\n" * 6
                print self.intro
                print self.bearings
            elif action == "inventory" or action == "inv":
                print all_strings.line_break
                print "\n" * 4
                inv.show()
                print all_strings.action_prompt
            elif action == "sit" or action == "sit down":
                print all_strings.action_sit
            elif action == "stand":
                print all_strings.action_stand
            elif action == "wait":
                print all_strings.action_wait
            elif action == "lie down":
                print all_strings.action_lie
            else:
                print "\nI'm sorry, but you can't %r.\n" % action
            action = raw_input("> ").lower()
        print "\nYou attempt to %s." % action
        sleep(0.75)
        return action

    def stone_available(self):
        if self.stone_here and self.solved and "take stone" not in self.good_moves:
            self.good_moves.append("take stone")
        else:
            pass

    def correct_intro(self):
        if self.visited == False:
            print self.intro
        self.visited = True
        if not self.current_room:
            print self.bearings
        elif self.current_room:
            print "\nWhat do you do?\n"
        self.current_room = True


class StartingRoom(Room):

    start_of_game = True
    good_moves = ['go north', 'walk north', 'take pen', 'touch pen',
                    'take mattress', 'touch mattress', 'lie down', 'sleep',
                    'take junk', 'touch junk']
    bad_moves = ['walk south', 'walk east', 'walk west', 'go south', 'go east',
                'go west']
    wake_up = all_strings.starting_room_wake_up
    extra = all_strings.starting_room_extra1
    intro = all_strings.starting_room_intro
    bearings = all_strings.starting_room_bearings1

    def enter(self):
        if self.start_of_game == True:
            print self.wake_up
            self.start_of_game = False
            self.visited = True
        self.correct_intro()
        action = self.action()

        if action == "go north" or action == "walk north":
            self.current_room = False
            return "middle"

        if action == "lie down" or action == "sleep":
            all_strings.starting_room_lie()
            return self.enter()

        if action == "touch pen":
            all_strings.starting_room_touch_pen()
            return self.enter()

        if action == "touch mattress":
            all_strings.starting_room_touch_mattress()
            return self.enter()

        if action == "take mattress":
            all_strings.starting_room_take_mattress()
            return self.enter()

        if action == "take junk":
            all_strings.starting_room_take_junk()
            return self.enter()

        if action == "touch junk":
            all_strings.starting_room_touch_junk()
            return self.enter()

        if action == "take pen":
            all_strings.starting_room_take_pen()
            self.good_moves.remove("take pen")
            inv.items.append("ballpoint pen")
            self.extra = all_strings.starting_room_extra2
            return self.enter()


class MiddleRoom(Room):

    good_moves = ['go east', 'walk east', 'walk south', 'walk east',
                    'walk west', 'go south', 'go east', 'go west', 'go north',
                    'walk north', 'touch newspapers', 'touch newspaper',
                    'take newspaper', 'take newspapers', 'touch rubber',
                    'take rubber']
    bad_moves = []
    intro = all_strings.middle_room_intro
    extra = all_strings.middle_room_extra
    bearings = all_strings.middle_room_bearings
    def enter(self):
        self.correct_intro()
        action = self.action()
        if action == "go south" or action == "walk south":
            self.current_room = False
            return "start"
        if action == "go east" or action == "walk east":
            self.current_room = False
            return "right"
        if action == "go west" or action == "walk west":
            self.current_room = False
            return "left"
        if action == "go north" or action == "walk north":
            self.current_room = False
            return "door"

        if action == "touch newspapers" or action == "touch newspaper":
            all_strings.middle_room_touch_newspaper()
            return self.enter()

        if action == "take newspapers" or action == "take newspaper":
            all_strings.middle_room_take_newspaper()
            return self.enter()

        if action == "touch rubber":
            all_strings.middle_room_touch_rubber()
            return self.enter()

        if action == "take rubber":
            all_strings.middle_room_take_rubber()
            return self.enter()


class TheDoor(Room):

    door_open = False
    attempted_door = False
    touched_indentations = False
    good_moves = ['touch door', 'place stones', 'back away', 'go back',
                    'walk south', 'go south', 'take bag', 'open door',
                    'go north', 'walk north', 'touch indentations',
                    'place stone', 'touch indentation', 'take indentations',
                    'take indentation']
    bad_moves = ['go east', 'walk east', 'go west', 'walk west']
    stones = {'Stone of Peace': False, 'Stone of Silence': False,
            'Stone of Respect': False, 'Stone of Practice': False,
            'Stone of Friendship': False, 'Stone of Compassion': False}
    intro = all_strings.the_door_intro
    extra = all_strings.the_door_extra1
    bearings = all_strings.the_door_bearings1

    def enter(self):
        self.correct_intro()
        action = self.action()

        if action == 'touch door':
            all_strings.the_door_touch_door()
            return self.enter()

        if action == "take indentation" or action == "take indentations":
            all_strings.the_door_take_indentations()
            return self.enter()

        if action == 'touch indentation' or action == 'touch indentations':
            all_strings.the_door_touch_indentations1()
            TheDoor.touched_indentations = True
            have_stone = False
            for stone in self.stones.keys():
                if stone in inv.items:
                    have_stone = True
            if have_stone:
                all_strings.the_door_have_stone()
                return self.enter()
            else:
                all_strings.the_door_no_stone()
                return self.enter()

        if action == 'place stones' or action == 'place stone':
            placed = False
            for stone in self.stones.keys():
                if stone in inv.items:
                    inv.remove(stone)
                    print """
You take The %s and place it the indentation where it fits best.""" % stone
                    self.stones[stone] = True
                    placed = True
                    sleep(2.2)
            if placed:
                return self.enter()
            if not placed:
                all_strings.the_door_not_placed()
                return self.enter()

        if (action == 'go south' or action == 'go back' or
            action == 'back away' or action == 'walk south'):
            self.current_room = False
            return 'middle'

        if action == 'take bag':
            all_strings.the_door_take_bag()
            inv.add_to_top('dirty bag')
            self.bag = False
            self.extra = all_strings.the_door_extra2
            return self.enter()

        if action == 'open door':
            if self.door_open:
                print all_strings.the_door_already_open
                return self.enter()
            if self.stone_count() > 3:
                if self.attempted_door:
                    all_strings.the_door_experienced()
                    self.door_open = True
                    self.bearings = all_strings.the_door_bearings2
                    return self.enter()
                else:
                    all_strings.the_door_cant_push()
                    action = "sink into deeper despair"
                    door_count = 0
                    while (action != "pull door" and action != "pull"
                            and door_count < 6):
                        door_count += 1
                        print "I guess you might as well %s." % action
                        action = raw_input("\nBut would you also like to try to do something else? > ")
                    all_strings.the_door_can_pull()
                    self.door_open = True
                    self.bearings = all_strings.the_door_bearings2
                    return self.enter()
            else:
                all_strings.the_door_struggles()
                self.attempted_door = True
                return self.enter()

        if action == 'go north' or action == 'walk north':
            if self.door_open:
                self.current_room = False
                return 'end'
            else:
                all_strings.the_door_believe()
                return self.enter()

    def stone_count(self):
        count = 0
        for stone in self.stones.keys():
            if self.stones[stone]:
                count += 1
        return count


class Left(Room):

    good_moves = ['go east', 'walk east', 'walk south', 'walk east',
                    'walk west', 'go south', 'go east', 'go west', 'go north',
                    'walk north', 'take frog', 'touch frog', 'catch frog']
    bad_moves = []
    intro = all_strings.left_intro
    extra = all_strings.left_extra
    bearings = all_strings.left_bearing
    def enter(self):
        self.correct_intro()
        action = self.action()
        if action == "go south" or action == "walk south":
            self.current_room = False
            return "battlefield"
        if action == "go east" or action == "walk east":
            self.current_room = False
            return "middle"
        if action == "go west" or action == "walk west":
            self.current_room = False
            return "dining room"
        if action == "go north" or action == "walk north":
            self.current_room = False
            return "butcher"

        if action == "take frog" or action == "touch frog":
            all_strings.left_take_frog()
            return self.enter()

        if action == "catch frog":
            all_strings.left_catch_frog()
            return self.enter()


class Right(Room):

    racetrack_open = True
    good_moves = ['go east', 'walk east', 'walk south', 'walk east',
                    'walk west', 'go south', 'go east', 'go west', 'go north',
                    'walk north', 'touch computer', 'touch computers']
    bad_moves = []
    intro = all_strings.right_intro
    extra = all_strings.right_extra
    bearings = all_strings.right_bearings
    def enter(self):
        self.correct_intro()
        action = self.action()
        if action == "go south" or action == "walk south":
            self.current_room = False
            return "world"
        if (action == "go east" or action == "walk east") and Right.racetrack_open:
            self.current_room = False
            return "racetrack"
        if (action == "go east" or action == "walk east" and
            not Right.racetrack_open):
            all_strings.right_racetrack_closed()
            return self.enter()
        if action == "go west" or action == "walk west":
            self.current_room = False
            return "middle"
        if action == "go north" or action == "walk north":
            self.current_room = False
            return "alone"
        if action == "touch computer" or action == "touch computers":
            all_strings.right_touch_computer()
            return self.enter()


class Battlefield(Room):

    stone_here = True
    good_moves = ['go north', 'walk north', 'talk to soldier', 'talk',
                'talk to her', 'touch soldier', 'take soldier']
    bad_moves = ['go east', 'walk east', 'walk south', 'walk west',
                'go south', 'go west', ]
    intro = all_strings.battlefield_intro
    extra = all_strings.battlefield_extra_start
    bearings = all_strings.battlefield_bearings1
    def enter(self):
        self.correct_intro()
        action = self.action()
        if action == "go north" or action == "walk north":
            self.current_room = False
            return "left"

        if action == "take soldier":
            all_strings.battlefield_take_soldier()
            return self.enter()

        if action == "touch soldier":
            all_strings.battlefield_touch_soldier()
            return self.enter()

        if (action == "talk" or action == "talk to soldier" or
            action == "talk to her"):
            all_strings.battlefield_riddle()
            solution = ""
            while self.guesses_left > 0 and not self.solved:
                print """
The soldier holds up her left hand, with %d digits up.""" % self.guesses_left
                self.guesses_left -= 1
                solution = raw_input("\nHow do you answer? > ").lower()
                if solution == "onion" or solution == "an onion":
                    self.solved = True
                if self.guesses_left == 1:
                    all_strings.battlefield_hint()
            self.bearings = all_strings.battlefield_bearings2
            if self.solved:
                self.extra = all_strings.battlefield_extra_win
                self.stone_available()
                print all_strings.battlefield_solved
            else:
                self.extra = all_strings.battlefield_extra_fail
                print all_strings.battlefield_failed
                inv.failed_puzzles += 1
                inv.end_if_failed()
            self.good_moves.remove("talk")
            self.good_moves.remove("talk to her")
            self.good_moves.remove("talk to soldier")
            sleep(4.5)
            return self.enter()

        if action == "take stone":

            if inv.stones_carried() >= 1 and "dirty bag" not in inv.items:
                all_strings.no_bag()
                return self.enter()

            if inv.stones_carried() == 0 or "dirty bag" in inv.items:
                self.stone_here = False
                inv.items.append("Stone of Respect")
                self.good_moves.remove("take stone")
                all_strings.stone_of_respect_pickup()
                if TheDoor.touched_indentations:
                    all_strings.indentation_hint()
                self.extra = all_strings.battlefield_extra_final
                return self.enter()


class DiningRoom(Room):

    stone_here = True
    good_moves = ['go east', 'walk east', 'read note', 'touch fountain',
                    'touch fountains', 'take fountain', 'take fountains',
                    'touch clock', 'touch grandfather clock', 'touch sofa',
                    'take sofa', 'look outside', 'touch curtains',
                    'touch curtain', 'sit on sofa', 'touch water', 'take water',
                    'take curtain', 'take curtains']
    bad_moves = ['go north', 'walk north', 'walk south', 'walk west',
                'go south', 'go west' ]
    intro = all_strings.dining_room_intro
    extra = all_strings.dining_room_extra_start
    bearings = all_strings.dining_room_bearings_start
    def enter(self):
        self.correct_intro()
        action = self.action()
        if action == "go east" or action == "walk east":
            self.current_room = False
            return "left"

        if (action == "touch fountains" or action == "touch fountain" or
            action == "touch water" or action == "take water"):
            all_strings.dining_room_touch_water()
            return self.enter()

        if action == "take fountains" or action == "take fountain":
            all_strings.dining_room_take_water()
            return self.enter()

        if action == "touch curtains" or action == "touch curtain":
            all_strings.dining_room_touch_curtain()
            return self.enter()

        if action == "take curtains" or action == "take curtain":
            all_strings.dining_room_take_curtain()
            return self.enter()

        if action == "sit on sofa":
            dining_room_sit()
            return self.enter()

        if action == "look outside":
            all_strings.dining_room_look_outside()
            return self.enter()

        if action == "touch clock" or action == "touch grandfather clock":
            all_strings.dining_room_touch_clock()
            return self.enter()

        if (action == "take clock" or action == "take grandfather clock" or
            action == "take sofa"):
            all_strings.dining_room_take_big()
            return self.enter()

        if action == "touch sofa":
            all_strings.dining_room_touch_sofa()
            return self.enter()

        if action == "read note":
            all_strings.dining_room_riddle()
            if "ballpoint pen" not in inv.items:
                all_strings.dining_room_no_pen()
                return self.enter()
            elif "ballpoint pen" in inv.items:
                all_strings.dining_room_yes_pen()
                solution = ""
                while self.guesses_left > 0 and not self.solved:
                    print """
Below the note there are still %d lines that are not used up.""" % self.guesses_left
                    self.guesses_left -= 1
                    solution = raw_input("\nWhat do you write? > ").lower()
                    if solution == "silence":
                        self.solved = True
                    if self.guesses_left == 1:
                        all_strings.dining_room_hint()
            self.bearings = all_strings.dining_room_bearings_after
            if self.solved:
                self.extra = all_strings.dining_room_extra_win
                self.stone_available()
                all_strings.dining_room_quiet()
            else:
                self.extra = all_strings.dining_room_extra_fail
                print all_strings.dining_room_failed
                inv.failed_puzzles += 1
                inv.end_if_failed()
            all_strings.dining_room_leave_pen()
            inv.remove("ballpoint pen")
            self.good_moves.remove("read note")
            return self.enter()

        if action == "take stone":

            if inv.stones_carried() >= 1 and "dirty bag" not in inv.items:
                all_strings.no_bag()
                return self.enter()

            if inv.stones_carried() == 0 or "dirty bag" in inv.items:
                self.stone_here = False
                inv.items.append("Stone of Silence")
                self.good_moves.remove("take stone")
                all_strings.stone_of_silence_pickup()
                if TheDoor.touched_indentations:
                    all_strings.indentation_hint()
                self.extra = all_strings.dining_room_extra_final
                self.bearings = all_strings.dining_room_bearings_final
                return self.enter()

class Butcher(Room):

    stone_here = True
    good_moves = ['go south', 'walk south', 'talk to butcher', 'talk',
                    'talk to man', 'talk to him', 'touch pig', 'take meat',
                    'take cut', 'take pig', 'touch meat', 'touch cut',
                    'take cuts', 'touch cuts', 'talk to the man']
    bad_moves = ['go north', 'walk north', 'walk east', 'walk west', 'go east',
                'go west']
    intro = all_strings.butcher_intro
    extra = all_strings.butcher_extra_start
    bearings = all_strings.butcher_bearings_start
    def enter(self):
        self.correct_intro()
        action = self.action()
        if action == "go south" or action == "walk south":
            self.current_room = False
            return "left"

        if action == "touch pig":
            all_strings.butcher_touch_pig()
            return self.enter()

        if (action == "touch cut" or action == "touch meat" or
            action == "touch cuts"):
            all_strings.butcher_touch_meat()
            self.good_moves.remove("touch cut")
            self.good_moves.remove("touch cuts")
            self.good_moves.remove("touch meat")
            return self.enter()

        if action == "take pig":
            all_strings.butcher_take_pig()
            self.good_moves.remove("take pig")
            return self.enter()

        if (action == "take meat" or action == "take cut" or
            action == "take cuts"):
            all_strings.butcher_take_meat()
            self.good_moves.remove("take cut")
            self.good_moves.remove("take meat")
            self.good_moves.remove("take cuts")
            return self.enter()

        if (action == "talk" or action == "talk to man" or
            action == "talk to butcher" or action == "talk to him" or
            action == "talk to the man"):
            for option in ["talk", "talk to him", "talk to butcher",
                            "talk to man", "talk to the man"]:
                self.good_moves.remove(option)
            all_strings.butcher_riddle()
            solution = ""
            while self.guesses_left > 0 and not self.solved:
                if self.guesses_left == 5:
                    print """
The man uses a small knife to carve a line into the wall behind him. There is
%d line in the wall. His lips seem to curl involuntarily.""" % (6 - self.guesses_left)
                else:
                    print """
The man uses a small knife to carve a line into the wall behind him. There are
%d lines in the wall. His lips seem to curl involuntarily.""" % (6 - self.guesses_left)
                self.guesses_left -= 1
                solution = raw_input("\nHow do you answer? > ").lower()
                if solution == "pillow" or solution == "a pillow":
                    self.solved = True
                if self.guesses_left == 1:
                    all_strings.butcher_hint()
            sleep(2)
            self.bearings = all_strings.butcher_bearings_after
            if self.solved:
                self.extra = all_strings.butcher_extra_win
                self.stone_available()
                print all_strings.butcher_solved
            else:
                self.extra = all_strings.butcher_extra_lose
                print all_strings.butcher_failed
                inv.failed_puzzles += 1
                inv.end_if_failed()
            sleep(4.5)
            return self.enter()

        if action == "take stone":

            if inv.stones_carried() >= 1 and "dirty bag" not in inv.items:
                all_strings.no_bag()
                return self.enter()

            if inv.stones_carried() == 0 or "dirty bag" in inv.items:
                self.stone_here = False
                inv.items.append("Stone of Peace")
                self.good_moves.remove("take stone")
                all_strings.stone_of_peace_pickup()
                if TheDoor.touched_indentations:
                    all_strings.indentation_hint()
                self.extra = all_strings.butcher_extra_final
                self.bearings = all_strings.butcher_bearings_final
                return self.enter()

class Racetrack(Room):

    stone_here = True
    good_moves = ['go west', 'walk west', 'talk', 'take rock', 'talk to robot',
                    'talk to human', 'talk to the robot', 'talk to the person',
                    'talk to the human', 'talk to human', 'talk to person',
                    'touch rock', 'take small rock']
    bad_moves = ['go north', 'walk north', 'walk east', 'walk south', 'go east',
                'go south']
    intro = all_strings.racetrack_intro
    extra = all_strings.racetrack_extra_start
    bearings = all_strings.racetrack_bearings_start
    def enter(self):
        self.correct_intro()
        action = self.action()
        if action == "go west" or action == "walk west":
            self.current_room = False
            return "right"

        if action == "touch rock":
            all_strings.racetrack_touch_rock()
            return self.enter()

        if action == "talk":
            all_strings.racetrack_talk()
            return self.enter()

        if action == "take rock" or action == "take small rock":
            all_strings.racetrack_take_rock()
            inv.add('rock')
            for option in ["take rock", "take small rock", "touch rock"]:
                self.good_moves.remove(option)
            for option in ["throw rock", "throw rock at person",
            "throw rock at human", "throw rock at the person",
            "throw rock at the robot", "throw rock at robot",
            "throw rock at hugbot"]:
                self.good_moves.append(option)
            self.extra = all_strings.racetrack_extra_no_rock
            return self.enter()

        if action == "throw rock":
            all_strings.racetrack_throw_rock()
            return self.enter()

        if action == "throw rock at human" or action == "throw rock at person":
            inv.remove('rock')
            all_strings.racetrack_throw_rock_at_human()
            inv.failed_puzzles += 1
            inv.end_if_failed()
            Right.racetrack_open = False
            return "right"

        if action == "talk to robot" or action == "talk to the robot":
            for option in ['talk to robot', 'talk to the robot']:
                self.good_moves.remove(option)
            all_strings.racetrack_talk_to_robot()
            return self.enter()

        if (action == "talk to human" or action == "talk to the human" or
            action == "talk to person" or action == "talk to the person"):
            all_strings.racetrack_talk_to_human()
            return self.enter()

        if (action == "throw rock at robot" or
        action == "throw rock at the robot" or
        action == "throw rock at hugbot"):
            inv.remove('rock')
            for option in ["throw rock", "throw rock at human",
            "throw rock at person", "throw rock at the human",
            "throw rock at the person", "throw rock at the robot",
            "throw rock at robot", "throw rock at hugbot"]:
                self.good_moves.remove(option)
            all_strings.racetrack_riddle()
            robot_clock = randint(1446, 1899)
            while self.guesses_left > 0 and not self.solved:
                self.guesses_left -= 1
                print """
'It's okay my friend, you are loved,' the hugbot says. You see the number %d
quickly counting down on the display that's (gently) pressing into your face.
""" % (((self.guesses_left + 1) * robot_clock) + randint(1, 100))
                solution = raw_input("What is the safeword? > ").lower()
                if solution == "fork" or solution == "a fork":
                    self.solved = True
                if self.guesses_left == 1:
                    all_strings.racetrack_hint()
            self.bearings = all_strings.racetrack_bearings_after
            if self.solved:
                self.extra = all_strings.racetrack_extra_win
                self.stone_available()
                all_strings.racetrack_solved()
            else:
                self.extra = all_strings.racetrack_extra_lose
                print all_strings.racetrack_failed
                inv.failed_puzzles += 1
                inv.end_if_failed()
            sleep(4.5)
            return self.enter()

        if action == "take stone":

            if inv.stones_carried() >= 1 and "dirty bag" not in inv.items:
                all_strings.no_bag()
                return self.enter()

            if inv.stones_carried() == 0 or "dirty bag" in inv.items:
                self.stone_here = False
                inv.items.append("Stone of Friendship")
                self.good_moves.remove("take stone")
                all_strings.stone_of_friendship_pickup()
                if TheDoor.touched_indentations:
                    all_strings.indentation_hint()
                self.extra = all_strings.racetrack_extra_final
                self.bearings = all_strings.racetrack_bearings_final
                return self.enter()

class Alone(Room):

    final_response = False
    good_text_up = False
    sad_text_up = False
    projector_power = False
    projector_on = False
    projector_open = False
    stone_here = True
    not_chatted = True
    good_moves = ['go south', 'walk south', 'talk', 'talk to lady',
                    'talk to her', 'talk to woman', 'talk to projector',
                    'talk to girl', 'plug in projector', 'turn on projector',
                    'open lid', 'open projector lid', 'look at projector',
                    'turn off projector', 'look at the projector', 'close lid',
                    'close projector lid', 'turn on the projector',
                    'turn off the projector', 'plug in the projector',
                    'unplug the projector', 'talk to the projector',
                    'unplug projector', 'look under projector',
                    'look under the projector']
    bad_moves = ['go north', 'walk north', 'walk east', 'walk west', 'go east',
                'go west']
    intro = all_strings.alone_intro
    extra = all_strings.alone_extra_start
    bearings = all_strings.alone_bearings_start
    def enter(self):
        self.correct_intro()

        if (self.projector_on and self.projector_open and self.not_chatted):
            all_strings.alone_riddle()
            while self.guesses_left > 0 and not self.solved:
                self.loading(self.guesses_left)
                self.guesses_left -= 1
                solution = raw_input("\n?? > ").lower()
                if solution == "shoe" or solution == "a shoe":
                    self.solved = True
                if self.guesses_left == 1:
                    all_strings.alone_hint()
            if self.solved:
                self.good_text_up = True
                self.extra = all_strings.alone_extra_win
                all_strings.alone_solved()
            else:
                self.sad_text_up = True
                self.extra = all_strings.alone_extra_lose
                all_strings.alone_failed()
                inv.failed_puzzles += 1
                inv.end_if_failed()
            sleep(3)
            self.not_chatted = False
            return self.enter()

        action = self.action()

        if action == "go south" or action == "walk south":
            self.current_room = False
            return "right"

        if (action == "talk" or action == "talk to lady" or
            action == "talk to her" or action == "talk to woman"):
            all_strings.alone_talk_to_lady()
            return self.enter()

        if action == "talk to projector" or action == "talk to the projector":
            all_strings.alone_talk_to_projector()
            return self.enter()

        if action == "talk to girl":
            all_strings.alone_talk_to_girl()
            return self.enter()

        if action == "plug in projector" or action == "plug in the projector":
            if self.projector_power:
                all_strings.alone_projector_powered()
                return self.enter()
            self.projector_power = True
            all_strings.alone_projector_power_on()
            return self.enter()

        if action == "unplug projector" or action == "unplug the projector":
            if not self.projector_power:
                all_strings.alone_projector_unpowered()
                return self.enter()
            self.projector_power = False
            self.projector_on = False
            all_strings.alone_projector_power_off()
            if self.stone_here:
                self.extra = all_strings.alone_extra_proj_off
            return self.enter()

        if action == "turn on projector" or action == "turn on the projector":
            if self.projector_on:
                all_strings.alone_projector_running()
                return self.enter()
            if self.projector_power:
                all_strings.alone_projector_turn_on()
                self.projector_on = True
                if self.final_response:
                    self.extra = all_strings.alone_extra_final
                elif self.good_text_up:
                    self.extra = all_strings.alone_extra_win
                elif self.sad_text_up:
                    self.extra = all_strings.alone_extra_lose
                return self.enter()
            elif not self.projector_power:
                all_strings.alone_projector_no_power()
                return self.enter()

        if action == "turn off projector" or action == "turn off the projector":
            if not self.projector_on:
                all_strings.alone_projector_was_off()
                return self.enter()
            self.projector_on = False
            all_strings.alone_projector_turn_off()
            if self.stone_here:
                self.extra = all_strings.alone_extra_proj_off
            return self.enter()

        if action == "look at projector" or action == "look at the projector":
            all_strings.alone_proj_look_basic()
            if not self.projector_open:
                all_strings.alone_proj_look_lid()
            if not self.projector_on:
                all_strings.alone_proj_look_on()
            if not self.projector_power:
                all_strings.alone_proj_look_power()
            return self.enter()

        if action == "open lid" or action == "open projector lid":
            if self.projector_open:
                all_strings.alone_projector_no_lid()
                return self.enter()
            self.projector_open = True
            all_strings.alone_projector_open()
            return self.enter()

        if action == "close lid" or action == "close projector lid":
            if not self.projector_open:
                all_strings.alone_projector_lid()
                return self.enter()
            self.projector_open = False
            all_strings.alone_projector_close()
            return self.enter()

        if (action == "look under projector" or
        action == "look under the projector"):
            if not self.solved:
                all_strings.alone_look_under_start()
                return self.enter()
            elif self.stone_here and self.solved:
                self.stone_available()
                all_strings.alone_look_under_solved()
                return self.enter()
            else:
                all_strings.alone_look_under_final()
                return self.enter()

        if action == "take stone":

            if inv.stones_carried() >= 1 and "dirty bag" not in inv.items:
                all_strings.no_bag()
                return self.enter()

            if inv.stones_carried() == 0 or "dirty bag" in inv.items:
                self.stone_here = False
                inv.items.append("Stone of Compassion")
                self.good_moves.remove("take stone")
                all_strings.stone_of_compassion_pickup()
                if TheDoor.touched_indentations:
                    all_strings.indentation_hint()
                self.final_response = True
                self.extra = all_strings.alone_extra_final
                self.bearings = all_strings.alone_bearings_final
                return self.enter()

    def loading(self, count):
        for i in xrange(count):
            sleep(1)
            print "\n."

class World(Room):

    stone_here = True
    good_moves = ['go north', 'walk north', 'talk', 'talk to elephant',
                'talk to it', 'sit', 'sit cross-legged', 'sit on rock',
                'touch elephant', 'touch rock', 'talk to rock',
                'enjoy the view', 'look at mountains', 'fan yourself',
                'enjoy the amazing view']
    bad_moves = ['go east', 'walk east', 'walk south', 'walk west',
                'go south', 'go west', ]
    intro = """
Incredible. This passage somehow led to the top of a mountain. The view is
better than any you have ever experienced. You feel miniscule. The mountains
speak of something out of The Cossacks by Tolstoy. The palette has oranges, deep
greens, light blues and everything in between mixed in. Perhaps more striking
is the tiny (relatively speaking) elephant sitting cross-legged in loose
clothing. The elephant is facing you, but its eyes do not open as you enter."""
    extra = """
There is an elephant sitting cross-legged in front of you. To your left is a
sizable rock. There is an amazing view to enjoy and many mountains to look at.
It is very hot."""
    bearings = """
To the north is the strangely incongruous passage that leads back to the office
from which you came.

What do you do?\n"""
    def enter(self):
        self.correct_intro()
        action = self.action()
        if action == "go north" or action == "walk north":
            self.current_room = False
            return "right"

        if action == "sit":
            if self.stone_here:
                print """
The ground is very hot from the sun."""
                sleep(3)
                print "\nThis sucks."
                sleep(2)
                print "\nYou get up."
                sleep(2)
                return self.enter()
            else:
                print "\nNot right now."
                sleep(2)
                return self.enter()

        if action == "sit cross-legged":
            if self.stone_here:
                print """
Trying to mirror the elephant exactly, you sit on the ground and cross your
legs."""
                sleep(4.5)
                print "\nYour right leg starts to cramp up."
                sleep(3)
                print "\nYou get up."
                sleep(2)
                return self.enter()
            else:
                print "\nThere is much to do."
                sleep(2)
                return self.enter()

        if action == "sit on rock":
            if self.stone_here:
                print """
It is pretty comfortable."""
                sleep(3)
                print "\nYou wonder what else you can see if you go walk around a bit."
                sleep(2)
                print "\nYou get up."
                sleep(2)
                return self.enter()
            else:
                print "\nYou don't feel tired."
                sleep(2)
                return self.enter()

        if action == "enjoy the view" or action == "enjoy the amazing view":
            if self.stone_here:
                print """
Simply breathtaking..."""
                sleep(6)
                print "\nYou wonder if some of the computers in the office have cable internet."
                sleep(2)
                print "\nYou're not really paying much attention any more."
                sleep(2)
                return self.enter()
            else:
                print "\nThe world is rich."
                sleep(2)
                return self.enter()

        if action == "look at mountains":
            if self.stone_here:
                print """
You feel tiny."""
                sleep(3)
                print "\nYou wonder how easy it would be to climb up one of those mountaints."
                sleep(2)
                print "\nYou'll do it someday."
                sleep(2)
                return self.enter()
            else:
                print "\n..."
                sleep(2)
                return self.enter()

        if action == "touch rock":
            if self.stone_here:
                print "\nJust another rock."
                sleep(2)
                return self.enter()
            else:
                print "\nIt feels as it should."
                sleep(2)
                return self.enter()

        if action == "talk to rock":
            if self.stone_here:
                print """
'How are you doing, rock?' you say."""
                sleep(3)
                print "\nOk..."
                sleep(1.5)
                return self.enter()
            else:
                print "\nWord are not what will help your mutual communication."
                sleep(3)
                return self.enter()

        if action == "fan yourself":
            if self.stone_here:
                print """
The effect is not worth the effort"""
                sleep(2)
                return self.enter()
            else:
                print "\nAs hot as it is, you know that you will survive."
                sleep(3)
                return self.enter()

        if action == "touch rock":
            if self.stone_here:
                print "\nJust another rock."
                sleep(2)
                return self.enter()
            else:
                print "\nIt feels as it should."
                sleep(2)
                return self.enter()

        if action == "touch elephant":
            print "\nSeems like a bad idea."
            sleep(2)
            return self.enter()

        if (action == "talk" or action == "talk to elephant" or
            action == "talk to it"):
            self.good_moves.remove("talk")
            self.good_moves.remove("talk to it")
            self.good_moves.remove("talk to elephant")
            self.good_moves.remove("touch elephant")
            print "\n'Hello,' you say."
            sleep(3)
            print "\nThe elephant opens its eyes."
            sleep(2)
            print """
'I am heavy but not backwards,' it intones."""
            sleep(3)
            print """
'What am I?'"""
            sleep(2)
            print "\nYou feel compelled to answer."
            sleep(1.5)
            solution = ""
            while self.guesses_left > 0 and not self.solved:
                sleep(1)
                self.overheating(self.guesses_left)
                self.guesses_left -= 1
                sleep(1)
                solution = raw_input("\nYou speak > ").lower()
                if solution == "ton":
                    self.solved = True
            if self.solved:
                self.extra = """
In front of you is a stone lying on the ground. Perhaps the stone is worth
picking up. To your left is a sizable rock. There is an amazing view to enjoy
and many mountains to look at. It is very hot."""
                self.stone_available()
                sleep(1)
                print """
You blink and the elephant is gone. It seems like there is hardly a trace of it.
There is some small object where it elephant appeared to be."""
            else:
                self.extra = """
Where the elephant was there is now nothing. To your left is a sizable rock.
There is an amazing view to enjoy and many mountains to look at. It is very hot."""
                print """
You blink and the elephant is gone. There is no trace of it."""
                inv.failed_puzzles += 1
                inv.end_if_failed()
            sleep(2.5)
            self.intro = """
Incredible. This passage somehow led to the top of a mountain. The view in
better than any you have ever experienced. You feel miniscule. The mountains
speak of something out of The Cossacks by Tolstoy. The palette has oranges, deep
greens, light blues and everything in between mixed in."""
            return self.enter()

        if action == "take stone":

            if inv.stones_carried() >= 1 and "dirty bag" not in inv.items:
                all_strings.no_bag()
                return self.enter()

            if inv.stones_carried() == 0 or "dirty bag" in inv.items:
                self.stone_here = False
                inv.items.append("Stone of Practice")
                self.good_moves.remove("take stone")
                print"""
You pick up the stone. You feel more sure of yourself. There is much that you
do not know, but there is much that can be seen, experienced and learned. On the
stone you see the word 'PRACTICE'."""
                sleep(5)
                if TheDoor.touched_indentations:
                    all_strings.indentation_hint()
                return self.enter()

    def overheating(self, count):
        if count == 5:
            print "\nYou feel sweat building up on your brow."
        if count == 4:
            print "\nYour clothes are starting to be sweat through."
        if count == 3:
            print "\nYou starting to feel like you're swimming in your clothes."
        if count == 2:
            print "\nThe heat is becoming oppressive."
        if count == 1:
            print "\nYou feel close to passing out."
        if count == 0:
            print "\nYou feel nauseous."
        else:
            pass


class End(Room):

    stories = {
    'Stone of Peace': """
May it help you find ease in the difficult life we all share. The odds are in
many ways stacked against us, but if we tread carefully and keep our well-being
as the ultimate goal, we can dance through. Knowing the way that leads to our
well-being takes more than common wisdom. May you have the humility and modesty
to not answer when you should ask.""",
    'Stone of Silence': """
One can hope it helps you it times when things seem chaotic and oppressive. When
things become dull or routine. When everthing loses its lustre. Silence might
remind you that nothing is required for perfection. This is easy to say but
seldom is it realized. May we all make the effort.""",
    'Stone of Respect': """
Let it remind you that each of us is here in the same way. Others have had a
different life. A different experience. But right now, in any given interaction
each is trying their best. To assume that less effort is given is to not give
the respect that is perhaps deserved. To ask for more is to ask a stone to sing.
We each of us are on different roads. May we not blame the traveller who
followed the false marker but rather show this traveller the marker we know is
best.""",
    'Stone of Practice': """
Perhaps you have already travelled far down the path you have chosen. Perhaps
you have only ever just begun. Let your strenght and perseverance lead you
further than you had dreamt. No one can walk on all the paths, but by knowing
one well, we can help others who would travel them. By knowing many we can act
as true sign posts who can help others choose. May you keep travelling for the
world needs many to walk and share their wisdom.""",
    'Stone of Friendship': """
Know that to travel alone is the greatest way to make that trite mistake of
over-commitment to a single invenstment. Share your joys to magnify them. Share
your sorrows to trivialize them. Laugh with close companions and let their joys
be your own. The wealth of such a life cannot be matched.""",
    'Stone of Compassion': """
Know that each of us carries sorrow and pain, from the richest to the poorest
soul. What one lacks another has in abundance, and no one has it all. Instead
of judging those that have what you have not because they have not what you
have, be a teacher and be a student. Show them the way. Not once, not one
hundred times, but as many times until their way becomes the Way. Not every soul
is a willing student. But neither is every willing student a soliciting soul.
May you find the judgement you need to help those you can, and leave those that
you cannot in peace."""}

    def enter(self):
        print """
You are standing in a tiny cell."""
        sleep(4)
        print """
The magnificent door behind you closes shut."""
        for stone in TheDoor.stones.keys():
            if TheDoor.stones[stone]:
                raw_input("Go on? > ")
                print "\nYou found the %s." % stone
                print self.stories[stone]
                print "\n" * 2
        raw_input("Ready to finish? > ")
        print """
Thank you for taking the time. It is appreciated.

If you noticed something that seemed like a bug or just have any comments,
or suggestions for improvements, please reach me at Andrei.Borissenko@gmail.com
I would love to hear from you."""
        exit(1)


class Map(object):

    rooms = {'start': StartingRoom(), 'middle': MiddleRoom(), 'door': TheDoor(),
            'left': Left(), 'right': Right(), 'butcher': Butcher(),
            'dining room': DiningRoom(), 'battlefield': Battlefield(),
            'racetrack': Racetrack(), 'alone': Alone(), 'world': World(),
            'end': End()}

    def play(self, next_room):
        print "\n" * 35
        return self.rooms[next_room].enter()

the_map = Map()
inv = Inventory()
game = Engine(the_map)
game.play('start')

# TODO: Get rid of string literals
# TODO: Refactor the stone pick ups to take the message upon pick up and the
# particular stone picked up to maybe avoid the large amounts of duplicate code
# TODO: Get the riddles failed counter to give some kind of message to indicate
# that players should try to not fail puzzles
# TODO: Add a way to save the game... its a bit long.
