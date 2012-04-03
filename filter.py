import pickle, sys

def stored_cases():
    kb_file = open('KB', 'r')
    kb = pickle.load(kb_file)
    kb_file.close()
    return kb

def write_stored_cases(kb):
    kb_file = open('KB', 'w')
    pickle.dump(kb, kb_file)
    kb_file.close()

def encode(file_stream):
    words = file_stream.split(' ')
    word_count =  {}
    for word in words:
        if word_count.has_key(word):
            word_count[word]+=1
        else:
            word_count[word] = 1
    return word_count

def get_nearest_match(wc, kb):
    nearest_match_index = 0
    max_points = 0.0
    for index, case in enumerate(kb):
        pts = 0.0
        for word in wc:
            if word in case['word_count']:
                dif = abs(wc[word]-case['word_count'][word])
                if dif == 0:
                    pts+=1
                elif dif<3:
                    pts+=0.8
                elif dif<5:
                    pts+=0.6
                elif dif<6:
                    pts+=0.4
                else:
                    pts+=0.3
        if pts > max_points:
            max_points = pts
            nearest_match_index = index
    return nearest_match_index

def main():
    if len(sys.argv) != 2:
        print 'Please supply the input filename'
        return
    kb = stored_cases()
    input_filename = sys.argv[1]
    input_file = open(input_filename, 'r')
    input_text = input_file.read()
    encoded_input = encode(input_text)
    nearest_match = get_nearest_match(encoded_input, kb)
    try:
        nm = kb[nearest_match]
        proposed_sol = nm['label']
    except:
        #kb is empty
        proposed_sol = 'GENUINE'
    print 'The input file is classified as ' + proposed_sol
    confirmation = raw_input('Is this classification correct?(y/n): ')
    if confirmation == 'y':
        label = proposed_sol
    elif confirmation == 'n':
        if proposed_sol == 'SPAM':
            label = 'GENUINE'
        elif proposed_sol == 'GENUINE':
            label = 'SPAM'
    new_case = {}
    new_case['label'] = label
    new_case['word_count'] = encoded_input
    confirmation = raw_input('Store the new case?(y/n): ')
    if confirmation == 'y':
        kb.append(new_case)
        write_stored_cases(kb)
    input_file.close()
    return

if __name__ == '__main__':
    main()
