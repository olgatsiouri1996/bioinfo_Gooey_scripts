# python3
from gooey import *
import sys
from pyfaidx import Fasta
# input parameters
@Gooey(required_cols=1, program_name= 'subset fasta records, ids or headers by fasta description', header_bg_color= '#DCDCDC', terminal_font_color= '#DCDCDC', terminal_panel_color= '#DCDCDC')
def main():
    ap = GooeyParser()
    ap.add_argument("-in", "--input", required=True, widget='FileChooser', help="input multi-fasta file")
    ap.add_argument("-one", "--match", required=False, type=str, help="word or phrase to search in each fasta header(no regular expression, differentiates between capital or non capital letters)")
    ap.add_argument("-many", "--matches", required=False,widget='FileChooser', help="1-column txt file with a word or phrase in each line to search in each fasta header(no regular expression, differentiates between capital or non capital letters)")
    ap.add_argument("-out", "--output", required=False, widget='FileSaver', help="output multi-fasta file. File can be appended")
    ap.add_argument("-headers", "--headers", required=False, widget='FileSaver', help="1 or 2-column tab seperated txt file to save the output fasta identifiers or full fasta headers respectively. File can be appended")
    ap.add_argument("-pro", "--program", required=False, type=int, default=1, widget='Dropdown', choices=[1,2,3], help="Program to choose: 1) collect fasta records with headers that match the pattern 2) collect only fasta identifiers, 3) collect full fasta headers(id and description are tab seperated).")
    ap.add_argument("-pat", "--patterns", required=False, type=str, default='one', widget='Dropdown', choices=['one','many'], help="number of patterns to search")
    args = vars(ap.parse_args())
    # main
   # create function to split the input sequence based on a specific number of characters(60)
    def split_every_60(s): return [str(s)[i:i+60] for i in range(0,len(str(s)),60)]
    # import fasta file
    features = Fasta(args['input'])
    if args['patterns']=='one':
        # choose program
        program = args['program']
        match program:
            case 1:
                # iterate input headers to extract sequences and export as multi-fasta
                sys.stdout = open(args['output'], 'a')
                for key in features.keys():
                    if args['match'] in features[key].long_name:
                        print(''.join([">",features[key].long_name]).replace('\r',''))
                        print('\n'.join(split_every_60(features[key][:].seq)))
                sys.stdout.close()
            case 2:
                # export to 1-column txt file
                with open(args['headers'], 'a') as filehandle:
                    for key in features.keys():
                        if args['match'] in features[key].long_name:
                            filehandle.write('%s\n' % key)
            case 3:
                # export to 1-column txt file
                with open(args['headers'], 'a') as filehandle:
                    for key in features.keys():
                        if args['match'] in features[key].long_name:
                            filehandle.write('%s\n' % '\t'.join([key,str(features[key].long_name).split(' ',1)[1]]))
    else:
        # import the txt file with words from headers you want to extract the sequence from the input fasta
        with open(args['matches'], 'r') as f:
            pat = f.readlines()
        pat = [x.strip() for x in pat]
        # choose program
        program = args['program']
        match program:
            case 1:
                # iterate input headers to extract sequences and export as multi-fasta
                sys.stdout = open(args['output'], 'a')
                for p in pat:
                    for key in features.keys():
                        if str(p) in features[key].long_name:
                            print(''.join([">",features[key].long_name]).replace('\r',''))
                            print('\n'.join(split_every_60(features[key][:].seq)))
                sys.stdout.close()
            case 2:
                # export to 1-column txt file
                with open(args['headers'], 'a') as filehandle:
                    for p in pat:
                        for key in features.keys():
                            if str(p) in features[key].long_name:
                                filehandle.write('%s\n' % key)
            case 3:
                # export to 1-column txt file
                with open(args['headers'], 'a') as filehandle:
                    for p in pat:
                        for key in features.keys():
                            if str(p) in features[key].long_name:
                                filehandle.write('%s\n' % '\t'.join([key,str(features[key].long_name).split(' ',1)[1]]))


if __name__ == '__main__':
    main()
