def load_cat_file(filename):
    votes = []
    with open(filename, 'r') as file:
        for line in file:
            if line.startswith("#") or line == '':
                continue
            count_part, ranking_part = line.split(': ')
            listRanks = ranking_part.strip().split(", ")
            r = []
            for ranking in listRanks:
                if ranking.startswith("{"):
                    sliced = ranking[1:-1].strip()
                    if sliced == "":
                        ints = []
                    else:
                        ints = [int(x) for x in sliced.split(",")]
                else:
                    ints = [int(ranking)]
                r.append(ints)
            votes.append((int(count_part), r))
    return votes
            
# the winner is the candidate, that has the most first place votes
def plurality_rule(votes):
    res = {}
    for (numVotes, listPref) in votes:
        for pref in listPref[0]:
            if pref in res:
                res[pref] += numVotes / len(listPref[0])
            else:
                res[pref] = numVotes / len(listPref[0])
    return dict(sorted(res.items(), key=lambda item: item[1], reverse=True))
    
#the winner is the candidate, that has the least amount of veto votes - these votes are given when you are the last preference
def anti_plurality_rule(votes):
    res = {}

    for (numVotes, listPref) in votes:
        for i in range(3):
            for pref in listPref[i]:
                if pref not in res:
                    res[pref] = 0

    for (numVotes, listPref) in votes:
        for pref in listPref[2]:
            if pref in res:
                res[pref] += numVotes / len(listPref[2])
            else:
                res[pref] = numVotes / len(listPref[2])
    return dict(sorted(res.items(), key=lambda item: item[1]))

def borda_rule(votes):
    res = {}

    for (numVotes, listPref) in votes:
        for i in range(3):
            for pref in listPref[i]:
                if pref not in res:
                    res[pref] = 0
    
    for (numVotes, listPref) in votes:
        for i in range(3):
            below_count = 0
            for j in range(i + 1, 3):
                below_count += len(listPref[j])

            for pref in listPref[i]:
                res[pref] += numVotes * below_count
    return dict(sorted(res.items(), key=lambda item: item[1], reverse=True))


def copeland_rule(votes):
    res = {}

    for (numVotes, listPref) in votes:
        for i in range(3):
            for pref in listPref[i]:
                if pref not in res:
                    res[pref] = 0

    for (numVotes, listPref) in votes:
        for i in range(3):
            below_count = 0
            current_count = len(listPref[i])
            for j in range(i + 1, 3):
                below_count += len(listPref[j])

            for pref in listPref[i]:
                res[pref] += numVotes * (below_count + 0.5 * (current_count - 1))
    return dict(sorted(res.items(), key=lambda item: item[1], reverse=True))    


def single_transferable_vote(votes):
    while True:
        # collect all remaining candidates
        remaining_candidates = set()
        for (numVotes, listPref) in votes:
            for group in listPref:
                for candidate in group:
                    remaining_candidates.add(candidate)

        if len(remaining_candidates) == 1:
            return list(remaining_candidates)[0]
        number_candidates_first_place = {candidate: 0 for candidate in remaining_candidates}

        for (numVotes, listPref) in votes:
            if len(listPref) == 0:
                continue
            first_group = listPref[0]
            if len(first_group) == 0:
                continue
            for candidate in first_group:
                number_candidates_first_place[candidate] += numVotes / len(first_group)

        fewest_votes_candidate = min(number_candidates_first_place, key=number_candidates_first_place.get)

        new_votes = []
        for (numVotes, listPref) in votes:
            new_listPref = []
            for group in listPref:
                new_group = [candidate for candidate in group if candidate != fewest_votes_candidate]
                if new_group:
                    new_listPref.append(new_group)
            new_votes.append((numVotes, new_listPref))

        votes = new_votes
        

def print_ranking_table(plurality, anti_plurality, borda, copeland):

    def get_ranks(d, reverse=True):
        keys = sorted(d, key=d.get, reverse=reverse)
        return {k: i + 1 for i, k in enumerate(keys)}

    p_ranks = get_ranks(plurality)
    a_ranks = get_ranks(anti_plurality, reverse=False)
    b_ranks = get_ranks(borda)
    c_ranks = get_ranks(copeland)

    print("Positions of candidates")
    print(f"\n{'Candidate':<12} {'Plurality':>10} {'Anti-Plur':>10} {'Borda':>10} {'Copeland':>10}")
    for cid in range(1, 12):
        print(f"{cid:<12} {p_ranks[cid]:>10} {a_ranks[cid]:>10} {b_ranks[cid]:>10} {c_ranks[cid]:>10}")

#
# votes = {(numberOfVotes, listOfThreeListsPreferences)}
#

def main():
    filename = "00073-00000002.cat"
    votes = load_cat_file(filename)

    print("Plurality:")
    print(plurality_rule(votes))

    print("Anti-Plurality (Veto):")
    print(anti_plurality_rule(votes))

    print("Borda:")
    print(borda_rule(votes))

    print("Copeland:")
    print(copeland_rule(votes))

    print("STV Winner:")
    print(single_transferable_vote(votes))

    print_ranking_table(plurality_rule(votes), anti_plurality_rule(votes), borda_rule(votes), copeland_rule(votes))


if __name__ == "__main__":
    main()