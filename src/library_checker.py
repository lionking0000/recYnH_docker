#
# last modified 2017-10-17 22:20
#
#
from scipy import stats
import numpy
import command_center
import math
#import rimage
import sys
import fasta

def BLASTN_NEW( argv ):
    '''
        parse blastn output and make ppi
    '''

    ppi_cnt_dic = {}
    read1_cnt_dic = {}
    read2_cnt_dic = {}
    read1_dic = {}
    read2_dic = {}
    '''
    ['M03766:33:000000000-AT3T3:1:1101:21081:6509', '113', 'NMI', '880', '36', '54S41M', 'IGF2', '452', '0', 'ATTTTGATCATATGACTGCTCTGTTTCATTTTTTTCAATAAACCCTTTACAATTAAGTGTTCTCTAGGTCAACCTCACATAGCATACTTTGAAGA', 'HHFFHHHHFDHHHGHHHHHHHHEHHHHHGGHFHGBHGHHGHHEG4GHHHHHHHHHHHHHFFFG3GEBGBFHHHHGHHHHHGHHFHFHGHHGHHHH', 'AS:i:82', 'XN:i:0', 'XM:i:0', 'XO:i:0', 'XG:i:0', 'NM:i:0', 'MD:Z:41', 'YS:i:174', 'YT:Z:DP']
    ['M03766:33:000000000-AT3T3:1:1101:21081:6509', '177', 'IGF2', '452', '36', '5S87M', 'NMI', '880', '0', 'TCTCTAGGCCAAACGTCACCGTCCCCTGATTGCTCTACCCACCCAAGACCCCGCCCACGGGGGCGCCCCCCCAGAGATGGCCAGCAATCGGA', '/BBB/BBBFFFEFFFEEFAFB?FFFFBFFFFFFFEB;@-DFFFFFFD@FFFFEFFFFAFFFFDAFGCGGHGGHHHHHHHFFHHHGFEGFHHH', 'AS:i:174', 'XN:i:0', 'XM:i:0', 'XO:i:0', 'XG:i:0', 'NM:i:0', 'MD:Z:87', 'YS:i:82', 'YT:Z:DP']^C
    '''
    #if len( sys.argv ) < 2:
    #    print "python SAM.py ../data/roth2016_control_set_plus_control.fa output/2016-12-22_MiSeq/Friedrich/17543_S1.sam"
    #    sys.exit(0)
    total_cnt = 0
    fa = fasta.read_fasta_file( sys.argv[2] )
    filepath1 = sys.argv[3]
    filepath2 = sys.argv[4]

    print "# This file is generated by BLASTN_NEW"
    print "# The method is NEW"

    PREV_QNAME = ""
    f = open( filepath1 )
    read_cnt = 0
    for line in f.xreadlines():
        #if read_cnt % 10000 == 0: print read_cnt
        read_cnt += 1
        ## READ 1
        # @M03766:53:000000000-B63MG:1:1101:13982:1738  cask_p142       98.969  97      1       0       1       97      99      3       3.06e-50        184
        [ QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, SSTART, SEND, EVALUE, BITSCORE ] = line[:-1].split("\t")
        if QNAME == PREV_QNAME: continue
        if int( SEND ) > int ( SSTART ): continue # DEFAULT CONDITION. ==> 1968532 for 2016-12-22_MiSeq/Blastn/17543_S1.ppi.txt
        if int( QSTART ) > 10 or int( SSTART ) < 90: continue ## NEW CONDITION. 2017-10-13 => 1878423
        #if int( QSTART ) >= 5 or int( SSTART ) <= 95: continue ## NEW3 CONDITION. 2017-10-21
        #if int( QSTART ) + int( SSTART ) < 90: continue # NEW4
        read1_dic[ QNAME ] = TARGET
        read1_cnt_dic[ TARGET ] = read1_cnt_dic.get( TARGET, 0 ) + 1
        PREV_QNAME = QNAME
    f.close()

    PREV_QNAME = ""
    read_cnt = 0
    f = open( filepath2 )
    for line in f.xreadlines():
        #if read_cnt % 10000 == 0: print read_cnt
        read_cnt += 1
        ## READ 2
        # @M03766:53:000000000-B63MG:1:1101:13982:1738  cask_p142       98.969  97      1       0       1       97      99      3       3.06e-50        184
        [ QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, SSTART, SEND, EVALUE, BITSCORE ] = line[:-1].split("\t")
        if QNAME == PREV_QNAME: continue
        if int( SEND ) > int ( SSTART ): continue # DEFAULT CONDITION. ==> 1968532 for 2016-12-22_MiSeq/Blastn/17543_S1.ppi.txt
        if int( QSTART ) > 10 or int( SSTART ) < 90: continue ## NEW CONDITION. 2017-10-13
        #if int( QSTART ) >= 5 or int( SSTART ) <= 95: continue ## NEW3 CONDITION. 2017-10-21
        #if int( QSTART ) + int( SSTART ) < 90: continue # NEW4
        read2_dic[ QNAME ] = TARGET
        read2_cnt_dic[ TARGET ] = read2_cnt_dic.get( TARGET, 0 ) + 1
        PREV_QNAME = QNAME
    f.close()

    for QNAME in read1_dic:
        TARGET2 = read2_dic.get( QNAME, "" )
        if TARGET2 == "": continue
        TARGET1 = read1_dic[ QNAME ]
        ppi_cnt_dic[ ( TARGET1, TARGET2 ) ] = ppi_cnt_dic.get( ( TARGET1, TARGET2 ), 0 ) + 1
        total_cnt += 1
    f.close()

    id_list = fa.keys()
    id_list.sort()

    print "DB(Read 1) \ AD(Read 2)\t"+"\t".join( id_list )
    for id1 in id_list:
        output = id1
        for id2 in id_list:
            cnt = ppi_cnt_dic.get( (id1, id2 ), 0 )
            output += "\t%d" % cnt
        print output

    # print total_cnt # only for debug

    # output/$1/Blastn/$2.blastn
    fout1 = open( "%s.cnt.txt" % filepath1, "w" )
    fout2 = open( "%s.cnt.txt" % filepath2, "w" )
    for id in id_list:
        print >> fout1, "%s\t%d" % ( id, read1_cnt_dic.get( id, 0 ) )
        print >> fout2, "%s\t%d" % ( id, read2_cnt_dic.get( id, 0 ) )
    fout1.close()
    fout2.close()


def BLASTN( argv ):  
    '''
        parse blastn output and make ppi
    '''

    ppi_cnt_dic = {}
    read1_cnt_dic = {}
    read2_cnt_dic = {}
    read1_dic = {}
    read2_dic = {}
    '''
    ['M03766:33:000000000-AT3T3:1:1101:21081:6509', '113', 'NMI', '880', '36', '54S41M', 'IGF2', '452', '0', 'ATTTTGATCATATGACTGCTCTGTTTCATTTTTTTCAATAAACCCTTTACAATTAAGTGTTCTCTAGGTCAACCTCACATAGCATACTTTGAAGA', 'HHFFHHHHFDHHHGHHHHHHHHEHHHHHGGHFHGBHGHHGHHEG4GHHHHHHHHHHHHHFFFG3GEBGBFHHHHGHHHHHGHHFHFHGHHGHHHH', 'AS:i:82', 'XN:i:0', 'XM:i:0', 'XO:i:0', 'XG:i:0', 'NM:i:0', 'MD:Z:41', 'YS:i:174', 'YT:Z:DP']
    ['M03766:33:000000000-AT3T3:1:1101:21081:6509', '177', 'IGF2', '452', '36', '5S87M', 'NMI', '880', '0', 'TCTCTAGGCCAAACGTCACCGTCCCCTGATTGCTCTACCCACCCAAGACCCCGCCCACGGGGGCGCCCCCCCAGAGATGGCCAGCAATCGGA', '/BBB/BBBFFFEFFFEEFAFB?FFFFBFFFFFFFEB;@-DFFFFFFD@FFFFEFFFFAFFFFDAFGCGGHGGHHHHHHHFFHHHGFEGFHHH', 'AS:i:174', 'XN:i:0', 'XM:i:0', 'XO:i:0', 'XG:i:0', 'NM:i:0', 'MD:Z:87', 'YS:i:82', 'YT:Z:DP']^C
    '''
    #if len( sys.argv ) < 2:
    #    print "python SAM.py ../data/roth2016_control_set_plus_control.fa output/2016-12-22_MiSeq/Friedrich/17543_S1.sam"
    #    sys.exit(0)
    total_cnt = 0
    fa = fasta.read_fasta_file( sys.argv[2] )
    filepath1 = sys.argv[3]
    filepath2 = sys.argv[4]

    print "# This file is generated by BLASTN"

    PREV_QNAME = ""
    f = open( filepath1 )
    read_cnt = 0
    for line in f.xreadlines():
        #if read_cnt % 10000 == 0: print read_cnt
        read_cnt += 1
        ## READ 1
        # @M03766:53:000000000-B63MG:1:1101:13982:1738	cask_p142	98.969	97	1	0	1	97	99	3	3.06e-50	184
        [ QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, SSTART, SEND, EVALUE, BITSCORE ] = line[:-1].split("\t")
        if QNAME == PREV_QNAME: continue
        if int( SEND ) > int ( SSTART ): continue # DEFAULT CONDITION. ==> 1968532 for 2016-12-22_MiSeq/Blastn/17543_S1.ppi.txt
        #if int( QSTART ) > 10 or int( SSTART ) < 90: continue ## NEW CONDITION. 2017-10-13 => 1878423
        #if int( QSTART ) >= 5 or int( SSTART ) <= 95: continue ## NEW3 CONDITION. 2017-10-21
        #if int( QSTART ) + int( SSTART ) < 90: continue # NEW4
        read1_dic[ QNAME ] = TARGET
        read1_cnt_dic[ TARGET ] = read1_cnt_dic.get( TARGET, 0 ) + 1
        PREV_QNAME = QNAME
    f.close()

    PREV_QNAME = ""
    read_cnt = 0
    f = open( filepath2 )
    for line in f.xreadlines():
        #if read_cnt % 10000 == 0: print read_cnt
        read_cnt += 1
        ## READ 2
        # @M03766:53:000000000-B63MG:1:1101:13982:1738  cask_p142       98.969  97      1       0       1       97      99      3       3.06e-50        184
        [ QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, SSTART, SEND, EVALUE, BITSCORE ] = line[:-1].split("\t")
        if QNAME == PREV_QNAME: continue
        if int( SEND ) > int ( SSTART ): continue # DEFAULT CONDITION. ==> 1968532 for 2016-12-22_MiSeq/Blastn/17543_S1.ppi.txt
        #if int( QSTART ) > 10 or int( SSTART ) < 90: continue ## NEW CONDITION. 2017-10-13
        #if int( QSTART ) >= 5 or int( SSTART ) <= 95: continue ## NEW3 CONDITION. 2017-10-21
        #if int( QSTART ) + int( SSTART ) < 90: continue # NEW4
        read2_dic[ QNAME ] = TARGET
        read2_cnt_dic[ TARGET ] = read2_cnt_dic.get( TARGET, 0 ) + 1
        PREV_QNAME = QNAME
    f.close()

    for QNAME in read1_dic:
        TARGET2 = read2_dic.get( QNAME, "" )
        if TARGET2 == "": continue
        TARGET1 = read1_dic[ QNAME ]
        ppi_cnt_dic[ ( TARGET1, TARGET2 ) ] = ppi_cnt_dic.get( ( TARGET1, TARGET2 ), 0 ) + 1
        total_cnt += 1
    f.close()

    id_list = fa.keys()
    id_list.sort()

    print "DB(Read 1) \ AD(Read 2)\t"+"\t".join( id_list )
    for id1 in id_list:
        output = id1
        for id2 in id_list:
            cnt = ppi_cnt_dic.get( (id1, id2 ), 0 )
            output += "\t%d" % cnt
        print output

    # print total_cnt # only for debug

    # output/$1/Blastn/$2.blastn
    fout1 = open( "%s.cnt.txt" % filepath1, "w" )
    fout2 = open( "%s.cnt.txt" % filepath2, "w" )
    for id in id_list:
        print >> fout1, "%s\t%d" % ( id, read1_cnt_dic.get( id, 0 ) )
        print >> fout2, "%s\t%d" % ( id, read2_cnt_dic.get( id, 0 ) )
    fout1.close()
    fout2.close()


'''
Added on 2018/03/28 for Barcoded sample (Sarah and Hannah)
'''
def BLASTN_BARCODE( argv ):  
    import Barcode
    '''
        parse blastn output and make ppi
    '''

    ppi_cnt_dic = {}
    read1_cnt_dic = {}
    read2_cnt_dic = {}
    read1_dic = {}
    read2_dic = {}
    '''
    ['M03766:33:000000000-AT3T3:1:1101:21081:6509', '113', 'NMI', '880', '36', '54S41M', 'IGF2', '452', '0', 'ATTTTGATCATATGACTGCTCTGTTTCATTTTTTTCAATAAACCCTTTACAATTAAGTGTTCTCTAGGTCAACCTCACATAGCATACTTTGAAGA', 'HHFFHHHHFDHHHGHHHHHHHHEHHHHHGGHFHGBHGHHGHHEG4GHHHHHHHHHHHHHFFFG3GEBGBFHHHHGHHHHHGHHFHFHGHHGHHHH', 'AS:i:82', 'XN:i:0', 'XM:i:0', 'XO:i:0', 'XG:i:0', 'NM:i:0', 'MD:Z:41', 'YS:i:174', 'YT:Z:DP']
    ['M03766:33:000000000-AT3T3:1:1101:21081:6509', '177', 'IGF2', '452', '36', '5S87M', 'NMI', '880', '0', 'TCTCTAGGCCAAACGTCACCGTCCCCTGATTGCTCTACCCACCCAAGACCCCGCCCACGGGGGCGCCCCCCCAGAGATGGCCAGCAATCGGA', '/BBB/BBBFFFEFFFEEFAFB?FFFFBFFFFFFFEB;@-DFFFFFFD@FFFFEFFFFAFFFFDAFGCGGHGGHHHHHHHFFHHHGFEGFHHH', 'AS:i:174', 'XN:i:0', 'XM:i:0', 'XO:i:0', 'XG:i:0', 'NM:i:0', 'MD:Z:87', 'YS:i:82', 'YT:Z:DP']^C
    '''
    #if len( sys.argv ) < 2:
    #    print "python SAM.py ../data/roth2016_control_set_plus_control.fa output/2016-12-22_MiSeq/Friedrich/17543_S1.sam"
    #    sys.exit(0)
    total_cnt = 0
    fa = fasta.read_fasta_file( sys.argv[2] )
    filepath1 = sys.argv[3]
    filepath2 = sys.argv[4]

    print "# This file is generated by BLASTN"

    fa_filepath1 = filepath1[:-6] + "fa"
    fa_filepath2 = filepath2[:-6] + "fa"

    read1_barcode_id_dic = Barcode.IdentifyBarcodedSeq( fa_filepath1 )
    read2_barcode_id_dic = Barcode.IdentifyBarcodedSeq( fa_filepath2 ) 
    barcode_dic = Barcode.GetBarcodeDic()


    PREV_QNAME = ""
    f = open( filepath1 )
    read_cnt = 0
    for line in f.xreadlines():
        #if read_cnt % 10000 == 0: print read_cnt
        read_cnt += 1
        ## READ 1
        # @M03766:53:000000000-B63MG:1:1101:13982:1738	cask_p142	98.969	97	1	0	1	97	99	3	3.06e-50	184
        [ QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, SSTART, SEND, EVALUE, BITSCORE ] = line[:-1].split("\t")
        if QNAME == PREV_QNAME: continue
        if QNAME in read1_barcode_id_dic:
            TARGET = read1_barcode_id_dic[ QNAME ]
            read1_dic[ QNAME ] = TARGET
            read1_cnt_dic[ TARGET ] = read1_cnt_dic.get( TARGET, 0 ) + 1
            PREV_QNAME = QNAME
            continue        
        if int( SEND ) > int ( SSTART ): continue # DEFAULT CONDITION. ==> 1968532 for 2016-12-22_MiSeq/Blastn/17543_S1.ppi.txt
        #if int( QSTART ) > 10 or int( SSTART ) < 90: continue ## NEW CONDITION. 2017-10-13 => 1878423
        #if int( QSTART ) >= 5 or int( SSTART ) <= 95: continue ## NEW3 CONDITION. 2017-10-21
        #if int( QSTART ) + int( SSTART ) < 90: continue # NEW4      
        read1_dic[ QNAME ] = TARGET
        read1_cnt_dic[ TARGET ] = read1_cnt_dic.get( TARGET, 0 ) + 1
        PREV_QNAME = QNAME
    f.close()

    PREV_QNAME = ""
    read_cnt = 0
    f = open( filepath2 )
    for line in f.xreadlines():
        #if read_cnt % 10000 == 0: print read_cnt
        read_cnt += 1
        ## READ 2
        # @M03766:53:000000000-B63MG:1:1101:13982:1738  cask_p142       98.969  97      1       0       1       97      99      3       3.06e-50        184
        [ QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, SSTART, SEND, EVALUE, BITSCORE ] = line[:-1].split("\t")
        if QNAME == PREV_QNAME: continue
        if QNAME in read2_barcode_id_dic:
            TARGET = read2_barcode_id_dic[ QNAME ]
            read2_dic[ QNAME ] = TARGET
            read2_cnt_dic[ TARGET ] = read2_cnt_dic.get( TARGET, 0 ) + 1
            PREV_QNAME = QNAME
            continue
        if int( SEND ) > int ( SSTART ): continue # DEFAULT CONDITION. ==> 1968532 for 2016-12-22_MiSeq/Blastn/17543_S1.ppi.txt
        #if int( QSTART ) > 10 or int( SSTART ) < 90: continue ## NEW CONDITION. 2017-10-13
        #if int( QSTART ) >= 5 or int( SSTART ) <= 95: continue ## NEW3 CONDITION. 2017-10-21
        #if int( QSTART ) + int( SSTART ) < 90: continue # NEW4
        read2_dic[ QNAME ] = TARGET
        read2_cnt_dic[ TARGET ] = read2_cnt_dic.get( TARGET, 0 ) + 1
        PREV_QNAME = QNAME
    f.close()

    for QNAME in read1_dic:
        TARGET2 = read2_dic.get( QNAME, "" )
        if TARGET2 == "": continue
        TARGET1 = read1_dic[ QNAME ]
        ppi_cnt_dic[ ( TARGET1, TARGET2 ) ] = ppi_cnt_dic.get( ( TARGET1, TARGET2 ), 0 ) + 1
        total_cnt += 1
    f.close()

    id_list = fa.keys()
    id_list.extend( barcode_dic.values() )
    id_list.sort()

    print "DB(Read 1) \ AD(Read 2)\t"+"\t".join( id_list )
    for id1 in id_list:
        output = id1
        for id2 in id_list:
            cnt = ppi_cnt_dic.get( (id1, id2 ), 0 )
            output += "\t%d" % cnt
        print output

    # print total_cnt # only for debug

    # output/$1/Blastn/$2.blastn
    fout1 = open( "%s.cnt.txt" % filepath1, "w" )
    fout2 = open( "%s.cnt.txt" % filepath2, "w" )
    for id in id_list:
        print >> fout1, "%s\t%d" % ( id, read1_cnt_dic.get( id, 0 ) )
        print >> fout2, "%s\t%d" % ( id, read2_cnt_dic.get( id, 0 ) )
    fout1.close()
    fout2.close()


# New 22
def BLASTN_22( argv ):
    '''
        parse blastn output and make ppi
    '''

    ppi_cnt_dic = {}
    read1_cnt_dic = {}
    read2_cnt_dic = {}
    read1_dic = {}
    read2_dic = {}
    '''
    ['M03766:33:000000000-AT3T3:1:1101:21081:6509', '113', 'NMI', '880', '36', '54S41M', 'IGF2', '452', '0', 'ATTTTGATCATATGACTGCTCTGTTTCATTTTTTTCAATAAACCCTTTACAATTAAGTGTTCTCTAGGTCAACCTCACATAGCATACTTTGAAGA', 'HHFFHHHHFDHHHGHHHHHHHHEHHHHHGGHFHGBHGHHGHHEG4GHHHHHHHHHHHHHFFFG3GEBGBFHHHHGHHHHHGHHFHFHGHHGHHHH', 'AS:i:82', 'XN:i:0', 'XM:i:0', 'XO:i:0', 'XG:i:0', 'NM:i:0', 'MD:Z:41', 'YS:i:174', 'YT:Z:DP']
    ['M03766:33:000000000-AT3T3:1:1101:21081:6509', '177', 'IGF2', '452', '36', '5S87M', 'NMI', '880', '0', 'TCTCTAGGCCAAACGTCACCGTCCCCTGATTGCTCTACCCACCCAAGACCCCGCCCACGGGGGCGCCCCCCCAGAGATGGCCAGCAATCGGA', '/BBB/BBBFFFEFFFEEFAFB?FFFFBFFFFFFFEB;@-DFFFFFFD@FFFFEFFFFAFFFFDAFGCGGHGGHHHHHHHFFHHHGFEGFHHH', 'AS:i:174', 'XN:i:0', 'XM:i:0', 'XO:i:0', 'XG:i:0', 'NM:i:0', 'MD:Z:87', 'YS:i:82', 'YT:Z:DP']^C
    '''
    #if len( sys.argv ) < 2:
    #    print "python SAM.py ../data/roth2016_control_set_plus_control.fa output/2016-12-22_MiSeq/Friedrich/17543_S1.sam"
    #    sys.exit(0)
    total_cnt = 0
    fa = fasta.read_fasta_file( sys.argv[2] )
    filepath1 = sys.argv[3]
    filepath2 = sys.argv[4]

    PREV_QNAME = ""
    BLAST_TEMP = []
    f = open( filepath1 )
    read_cnt = 0
    for line in f.xreadlines():
        #if read_cnt % 10000 == 0: print read_cnt
        read_cnt += 1
        ## READ 1
        # @M03766:53:000000000-B63MG:1:1101:13982:1738	cask_p142	98.969	97	1	0	1	97	99	3	3.06e-50	184
        [ QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, SSTART, SEND, EVALUE, BITSCORE ] = line[:-1].split("\t")
        if QNAME != PREV_QNAME:
            if PREV_QNAME == "" or len( BLAST_TEMP ) == 0:
                BLAST_TEMP.append( [ int( QSTART ), QEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, SSTART, SEND, EVALUE, BITSCORE ] )
                PREV_QNAME = QNAME
                continue
            BLAST_TEMP.sort()
            [ _QSTART, _QEND, _QNAME, _TARGET, _PERCENT, _LENGTH, _MISMATCH, _GAPOPEN, _SSTART, _SEND, _EVALUE, _BITSCORE ] = BLAST_TEMP[0]
            if int( _SEND ) > int ( _SSTART ) or int ( _QEND ) < int( _QSTART ) or int( _QSTART ) > 10 or int( _SSTART ) < 90: # or int( _QSTART ) > 5: # int( _QEND ) - int( _QSTART ) < 40 : # or int( _QSTART ) > 10 or int( _SSTART ) < 90: 
                PREV_QNAME = QNAME
                #BLAST_TEMP = [] # [ [ int( SSTART ), SEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, EVALUE, BITSCORE ] ]
                BLAST_TEMP = [ [ int( QSTART ), QEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, SSTART, SEND, EVALUE, BITSCORE ] ]
                continue ## NEW CONDITION. 2017-10-13
            read1_dic[ _QNAME ] = _TARGET
            read1_cnt_dic[ _TARGET ] = read1_cnt_dic.get( _TARGET, 0 ) + 1
            PREV_QNAME = QNAME
            BLAST_TEMP = [ [ int( QSTART ), QEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, SSTART, SEND, EVALUE, BITSCORE ] ]
        else: # QNAME == PREV_QNAME
            BLAST_TEMP.append( [ int( QSTART ), QEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, SSTART, SEND, EVALUE, BITSCORE ] )
            PREV_QNAME = QNAME
            continue
        ''' 
        if QNAME == PREV_QNAME or PREV_QNAME == "": 
            BLAST_TEMP.append( [ int( SSTART ), SEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, EVALUE, BITSCORE ] )
            PREV_QNAME = QNAME
            continue
        else: 
            if len( BLAST_TEMP ) == 0:
                PREV_QNAME = QNAME
                BLAST_TEMP = [ [ int( SSTART ), SEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, EVALUE, BITSCORE ] ]
                continue
            BLAST_TEMP.sort( reverse = True )
            #print BLAST_TEMP
            [ _SSTART, _SEND, _QNAME, _TARGET, _PERCENT, _LENGTH, _MISMATCH, _GAPOPEN, _QSTART, _QEND, _EVALUE, _BITSCORE ] = BLAST_TEMP[0]
            if int( _SEND ) > int ( _SSTART ) or int ( _QEND ) < int( _QSTART ) or int( _QEND ) - int( _QSTART ) < 40 : # or int( _QSTART ) > 10 or int( _SSTART ) < 90: 
                PREV_QNAME = QNAME
                BLAST_TEMP = [] # [ [ int( SSTART ), SEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, EVALUE, BITSCORE ] ]
                continue ## NEW CONDITION. 2017-10-13
            read1_dic[ _QNAME ] = _TARGET
            read1_cnt_dic[ _TARGET ] = read1_cnt_dic.get( _TARGET, 0 ) + 1
            PREV_QNAME = QNAME
            BLAST_TEMP = [ [ int( SSTART ), SEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, EVALUE, BITSCORE ] ]
        ''' 
    f.close()
    if len( BLAST_TEMP ) != 0:
        BLAST_TEMP.sort()
        [ QSTART, QEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, SSTART, SEND, EVALUE, BITSCORE ] = BLAST_TEMP[0]
        if int( SEND ) > int ( SSTART ) or int ( QEND ) < int( QSTART ) or int( _QSTART ) > 10 or int( _SSTART ) < 90: # or int( QSTART ) > 5: 
            pass
        else:
            #if int( QSTART ) > 10 or int( SSTART ) < 90: ## NEW CONDITION. 2017-10-13
            #    pass
            #else: 
            read1_dic[ QNAME ] = TARGET
            read1_cnt_dic[ TARGET ] = read1_cnt_dic.get( TARGET, 0 ) + 1

    PREV_QNAME = ""
    BLAST_TEMP = []
    read_cnt = 0
    f = open( filepath2 )
    for line in f.xreadlines():
        #if read_cnt % 10000 == 0: print read_cnt
        read_cnt += 1
        ## READ 2
        # @M03766:53:000000000-B63MG:1:1101:13982:1738  cask_p142       98.969  97      1       0       1       97      99      3       3.06e-50        184
        [ QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, SSTART, SEND, EVALUE, BITSCORE ] = line[:-1].split("\t")
        if QNAME != PREV_QNAME:
            if PREV_QNAME == "" or len( BLAST_TEMP ) == 0:
                BLAST_TEMP.append( [ int( QSTART ), QEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, SSTART, SEND, EVALUE, BITSCORE ] )
                PREV_QNAME = QNAME
                continue
            BLAST_TEMP.sort()
            [ _QSTART, _QEND, _QNAME, _TARGET, _PERCENT, _LENGTH, _MISMATCH, _GAPOPEN, _SSTART, _SEND, _EVALUE, _BITSCORE ] = BLAST_TEMP[0]
            if int( _SEND ) > int ( _SSTART ) or int ( _QEND ) < int( _QSTART ) or int( _QSTART ) > 10 or int( _SSTART ) < 90: # or int( _QSTART ) > 5: #int( _QEND ) - int( _QSTART ) < 40 : # or int( _QSTART ) > 10 or int( _SSTART ) < 90: 
                PREV_QNAME = QNAME
                #BLAST_TEMP = [] # [ [ int( SSTART ), SEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, EVALUE, BITSCORE ] ]
                BLAST_TEMP = [ [ int( QSTART ), QEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, SSTART, SEND, EVALUE, BITSCORE ] ]
                continue ## NEW CONDITION. 2017-10-13
            read2_dic[ _QNAME ] = _TARGET
            read2_cnt_dic[ _TARGET ] = read2_cnt_dic.get( _TARGET, 0 ) + 1
            PREV_QNAME = QNAME
            BLAST_TEMP = [ [ int( QSTART ), QEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, SSTART, SEND, EVALUE, BITSCORE ] ]
        else: # QNAME == PREV_QNAME
            BLAST_TEMP.append( [ int( QSTART ), QEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, EVALUE, BITSCORE ] )
            PREV_QNAME = QNAME
            continue
        '''
        if QNAME == PREV_QNAME or PREV_QNAME == "": 
            BLAST_TEMP.append( [ int( SSTART ), SEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, EVALUE, BITSCORE ] )
            PREV_QNAME = QNAME
            continue
        else:
            if len( BLAST_TEMP ) == 0:
                PREV_QNAME = QNAME
                BLAST_TEMP = [ [ int( SSTART ), SEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, EVALUE, BITSCORE ] ]
                continue
            BLAST_TEMP.sort( reverse = True )
            #print BLAST_TEMP
            [ _SSTART, _SEND, _QNAME, _TARGET, _PERCENT, _LENGTH, _MISMATCH, _GAPOPEN, _QSTART, _QEND, _EVALUE, _BITSCORE ] = BLAST_TEMP[0]  
            if int( _SEND ) > int ( _SSTART )  or int ( _QEND ) < int( _QSTART )  or int( _QEND ) - int( _QSTART ) < 40  : # or int( _QSTART ) > 10 or int( _SSTART ) < 90: 
                PREV_QNAME = QNAME
                BLAST_TEMP = [] # [ [ int( SSTART ), SEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, EVALUE, BITSCORE ] ]
                continue ## NEW CONDITION. 2017-10-13
            read2_dic[ _QNAME ] = _TARGET
            read2_cnt_dic[ _TARGET ] = read2_cnt_dic.get( _TARGET, 0 ) + 1
            PREV_QNAME = QNAME
            BLAST_TEMP = [ [ int( SSTART ), SEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, QSTART, QEND, EVALUE, BITSCORE ] ]
        '''
    f.close()
    if len( BLAST_TEMP ) != 0:
        BLAST_TEMP.sort() 
        [ QSTART, QEND, QNAME, TARGET, PERCENT, LENGTH, MISMATCH, GAPOPEN, SSTART, SEND, EVALUE, BITSCORE ] = BLAST_TEMP[0]
        if int( SEND ) > int ( SSTART ) or int ( QEND ) < int( QSTART ) or int( _QSTART ) > 10 or int( _SSTART ) < 90: # or int( QSTART ) > 5:  
            pass
        else:
            #if int( QSTART ) > 10 or int( SSTART ) < 90: ## NEW CONDITION. 2017-10-13
            #    pass
            #else: 
            read2_dic[ QNAME ] = TARGET
            read2_cnt_dic[ TARGET ] = read2_cnt_dic.get( TARGET, 0 ) + 1

    for QNAME in read1_dic:
        TARGET2 = read2_dic.get( QNAME, "" )
        if TARGET2 == "": continue
        TARGET1 = read1_dic[ QNAME ]
        ppi_cnt_dic[ ( TARGET1, TARGET2 ) ] = ppi_cnt_dic.get( ( TARGET1, TARGET2 ), 0 ) + 1
        total_cnt += 1
    f.close()

    fa = fasta.read_fasta_file( sys.argv[2] )
    id_list = fa.keys()
    id_list.sort()

    print "DB(Read 1) \ AD(Read 2)\t"+"\t".join( id_list )
    for id1 in id_list:
        output = id1
        for id2 in id_list:
            cnt = ppi_cnt_dic.get( (id1, id2 ), 0 )
            output += "\t%d" % cnt
        print output

    # print total_cnt # only for debug

    # output/$1/Blastn/$2.blastn
    fout1 = open( "%s.cnt.txt" % filepath1, "w" )
    fout2 = open( "%s.cnt.txt" % filepath2, "w" )
    for id in id_list:
        print >> fout1, "%s\t%d" % ( id, read1_cnt_dic.get( id, 0 ) )
        print >> fout2, "%s\t%d" % ( id, read2_cnt_dic.get( id, 0 ) )
    fout1.close()
    fout2.close()


def TrimFastqToFastq( argv ):
    from fusion_ppi import ReadSequenceFile

    trimN = int( argv[2] )
    fastq = argv[3]
    read1 = ReadSequenceFile( fastq )

    for line in read1.stdout.xreadlines():
        print ">%s" % line[:-1]
        print read1.stdout.next()[trimN:-1]
        print read1.stdout.next()[:-1]
        print read1.stdout.next()[trimN:-1]

    read1.stdout.close()
    read1.kill()

def CheckHomoDimer( argv ):
    '''
Col	Field	Type	Brief Description
1	QNAME	String	Query template NAME
2	FLAG	Int	bitwise FLAG
3	RNAME	String	References sequence NAME
4	POS	Int	1- based leftmost mapping POSition
5	MAPQ	Int	MAPping Quality
6	CIGAR	String	CIGAR String
7	RNEXT	String	Ref. name of the mate/next read
8	PNEXT	Int	Position of the mate/next read
9	TLEN	Int	observed Template LENgth
10	SEQ	String	segment SEQuence
11	QUAL	String	ASCII of Phred-scaled base QUALity+33
    '''
    samfile = argv[2]
    gene = argv[3]

    #output/2017-08-22_MiSeq/Sebastian/S64_SQD_full.sam
    f = open( samfile )
    for line in f.xreadlines():
        if line[:3] in [ "@HD", "@SQ" ]: continue
        if line[:3] == "@PG": break
    for line in f.xreadlines():
        fields1 = line.split("\t")
        fields2 = f.next().split("\t")
        if fields1[1] != "113" or fields2[1] != "177": continue
        TARGET1 = fields1[2]
        TARGET2 = fields2[2]
        if TARGET1 == gene and TARGET2 == gene:
            print fields1[:11]
            print fields2[:11]
            print ""
    f.close()



def SamToMatrix( argv ):
    #samtools view -bS -f 113 output/2017-11-03_MiSeq/Sebastian/S1_W.sam | samtools sort - output/2017-11-03_MiSeq/Sebastian/S1_W.sorted
    #@M03766:70:000000000-BH6F4:1:1101:12554:1950	113	REEP2	2	41	97M	SARNP	40	0	AAACCCATCAAAAAAGCGCCCAAAGCTGAGCCACTGGCTGCCAAGACGCTGAAGACCCGGCCCAAGAAGAAGACCTCTGGCGGGGGCGACTCAGCTT	DEG.C00E@DGFF<CC-C?HF??<?<1HHF@2<@0/?/22DB//BC<3?24FFE?//?EF/GFB444443@?B1?1/////E011A0GFEF3EA1BB	AS:i:184	XN:i:0	XM:i:2	XO:i:0	XG:i:0	NM:i:2	MD:Z:39T7A49	YS:i:93	YT:Z:DP
    #@M03766:70:000000000-BH6F4:1:1101:12554:1950	177	SARNP	40	41	36S59M	REEP2	2	0	CAGTACGGGAAAAGTGACAGACTAGAATAACTGTTCAACCGCAGAGGATACAGAGGCAAAGAAGAGGAAAAAAGCAGAGCGCTTAGAGATTGCCT	>/?///?121B1B1B2?1B1444FB444GFB43BF/>?//?3DHHF444B3HHGB3DDHHFGEFDF3/FB55FHGG?10A35555F5HGFEE0EB	AS:i:93	XN:i:0	XM:i:4	XO:i:0	XG:i:0	NM:i:4	MD:Z:4A30G12T1G8	YS:i:184	YT:Z:DP

    fa = fasta.read_fasta_file( sys.argv[2] )
    samfile = argv[3]

    ppi_cnt_dic = {}

    f = open( samfile )
    for line in f.xreadlines():
        if line[:3] in [ "@HD", "@SQ" ]: continue
        if line[:3] == "@PG": break
    for line in f.xreadlines():
        fields1 = line.split("\t")
        fields2 = f.next().split("\t")
        if fields1[1] != "113" or fields2[1] != "177": continue
        TARGET1 = fields1[2]
        TARGET2 = fields2[2]
        ppi_cnt_dic[ ( TARGET1, TARGET2 ) ] = ppi_cnt_dic.get( ( TARGET1, TARGET2 ), 0 ) + 1
    f.close()

    id_list = fa.keys()
    id_list.sort()

    print "DB(Read 1) \ AD(Read 2)\t"+"\t".join( id_list )
    for id1 in id_list:
        output = id1
        for id2 in id_list:
            cnt = ppi_cnt_dic.get( (id1, id2 ), 0 )
            output += "\t%d" % cnt
        print output



def TrimFastqToFasta( argv ):
    from fusion_ppi import ReadSequenceFile

    trimN = int( argv[2] )
    fastq = argv[3]
    read1 = ReadSequenceFile( fastq )

    for line in read1.stdout.xreadlines():
        print ">%s" % line[:-1]
        print read1.stdout.next()[trimN:-1]
        read1.stdout.next()
        read1.stdout.next()

    read1.stdout.close()
    read1.kill()


def FastqToFasta( argv ):
    '''
@M03766:53:000000000-B63MG:1:1101:12798:1849 1:N:0:4
AACGTAAAATGATATAAATATCAATATATTAAATTATATTTTGCATAAAAAACAGTCTACATAATACTGTAAATCACAACATATCCTGTCACT
+
AFGFHHHFHHFHH5FDGBGEGGBD55B4FG444BFG444FFF434B43433///?43BBD4B4?F44FGH44B443B33?/B1B?22?B1?12
    '''
    fastq = argv[2] 
    f = open( fastq )
    for line in f.xreadlines():
        print ">%s" % line[:-1]
        print f.next()[:-1]
        f.next()
        f.next()
    f.close()

        

def GenerateLastNts( argv ):
    filepath = argv[2]
    if len( argv ) >= 4:
        length = int( argv[3] )
    else:
        length = 30

    fa = fasta.read_fasta( filepath )

    lastXnt_dic = {}

    for id in fa:
        lastXnt = fa[id][-length:].upper()
        print ">%s\n%s" % ( id, lastXnt ) #, lastXnt in lastXnt_dic
        lastXnt_dic[ lastXnt ] = id


def CheckLastNts( argv ):
    filepath = argv[2]

    fa = fasta.read_fasta( filepath )

    lastXnt_dic = {}

    for id in fa:
        lastXnt = fa[id][-30:].upper()
        if lastXnt in lastXnt_dic:
            print "############# \t", lastXnt, "\t", lastXnt_dic[ lastXnt ], "\t", id #">%s\n%s" % ( id, lastXnt ) #, lastXnt in lastXnt_dic
        else:
            lastXnt_dic[ lastXnt ] = id
            print "# \t", id, " insert", lastXnt


def CompareLastNts( argv ):
    filepath1 = argv[2]
    filepath2 = argv[3]

    fa1 = fasta.read_fasta( filepath1 )
    fa2 = fasta.read_fasta( filepath2 )

    lastXnt_dic1 = {}
    lastXnt_dic2 = {}

    for id in fa1:
        lastXnt = fa1[id][-30:].upper()
        lastXnt_dic1[ lastXnt ] = id

    for id in fa2:
        lastXnt = fa2[id][-30:].upper()
        lastXnt_dic2[ lastXnt ] = id

    lastXnt_set = set( lastXnt_dic1.keys() )
    lastXnt_set.update( lastXnt_dic2.keys() )

    for lastXnt in lastXnt_set:
        print "#\t",lastXnt, "\t", lastXnt_dic1.get( lastXnt, "-" ), "\t", lastXnt_dic2.get( lastXnt, "-" )

if __name__ == "__main__":
    aCommand = command_center.Command()
    aCommand.AddCommand( "generate_last_nts", GenerateLastNts )
    aCommand.AddCommand( "compare_last_nts", CompareLastNts )
    aCommand.AddCommand( "check_last_nts", CheckLastNts )
    aCommand.AddCommand( "check_homo_dimer", CheckHomoDimer )

    aCommand.Run()

