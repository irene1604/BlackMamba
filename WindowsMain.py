############################################################
#############################################################
# Black Mamba orion and pegasus code iditor for Windows     #
# This version has currently two code iditors:              #
#                                                           #
#                                                           #
# * pegasus is the default editor                           #
# * orion is the optimized code editor with a syntaxis      #
#   color                                                   #
# basically we can use both without any problems because    #
# they work very well.                                      #
#                                                           #
#                                                           #
# * to select a terminal it's very simple, just do this     #
#                                                           #
#       * mamba --T orion                                   #
#       * mamba --T pegasus                                 #
#############################################################
############################################
# **created by : amiehe-essomba            #
# **updating by: amiehe-essomba            #
# ** copyright 2023 amiehe-essomba         #         
############################################
#############################################################

import sys, os
from script.LEXER.FUNCTION      import main
from script                     import control_string
from script.PARXER.WINParxer    import parxer
from script.STDIN.LinuxSTDIN    import bm_configure     as bm
from script.DATA_BASE           import data_base        as db
#from rich.console               import Console
from IDE.EDITOR                 import header
#console = Console()


class windows:
    def __init__(self, data_base : dict):
        # main data base
        self.data_base  = data_base
        # string module analyses 
        self.analyse    = control_string.STRING_ANALYSE(self.data_base, 1)

    def terminal(self, c: str = '', terminal_name : str = 'pegasus'):
        # input initialization
        self.input      = '{}>>>{} {}'.format(bm.fg.yellow_L, c, bm.init.reset)
        # root of input 
        self.main_input = '{}>>>{} {}'.format(bm.fg.yellow_L, c, bm.init.reset)
        # lenght of the root 
        self.length     = len(self.input)
        # index initialization 
        self.index      = self.length
        # sub length initialization 
        self.sub_length = len('{}{}{}'.format(bm.fg.yellow_L, c, bm.init.reset))
        # index char in Input 
        self.Index      = 0      
        # line        
        self.line       = 0    
        # key         
        self.key        = False  
        # String used in BM for calculations        
        self.mainString = ''      
        # String index      
        self.mainIndex  = 0    
        # save cursor position          
        self.cursor     = []
        # false if clean line is not activated else true
        self.clear_line = False         
        
        # write input initialized 
        sys.stdout.write(bm.string().syntax_highlight(name=self.input))
        #flush 
        sys.stdout.flush()
        
        while True:
            try:
                # get an input 
                self.char = bm.read().readchar()
                #print(self.char)
                if self.char not in {10, 13}:
                    # clear entire line
                    if self.char == 12:
                        # move cursor left 
                        sys.stdout.write(bm.move_cursor.LEFT(pos=1000))
                        # clear entire line 
                        sys.stdout.write(bm.clear.line(pos=2))
                        # write input
                        sys.stdout.write(self.main_input)
                        #move cursor left again
                        sys.stdout.write(bm.move_cursor.LEFT(pos=1000))
                        
                        # block init
                        self.input      = self.main_input
                        self.index      = self.length
                        self.key        = False
                        self.mainString = ''
                        self.mainIndex  = 0
                        self.clear_line = True
                    # clear entire screen
                    elif self.char == 19:
                        #os.system('cls')
                        sys.stdout.write(bm.clear.screen(pos=2))
                        sys.stdout.write(bm.save.restore)
                    # write char
                    else:
                        self.input       = self.input[ : self.index ] + chr( self.char ) + self.input[ self.index : ]
                        self.mainString  = self.mainString[ : self.mainIndex ] + chr( self.char ) + self.mainString[ self.mainIndex : ]
                        self.index       += 1
                        self.mainIndex   += 1
                    
                elif self.char in {10, 13}:  # enter
                    self.line += 1
                    sys.stdout.write(bm.move_cursor.LEFT(pos=1000))
                    
                    ####################################################################
                    if terminal_name == 'orion':
                        # Syntaxis color 
                        self.input = self.input[: self.length] + bm.init.bold + bm.words(string=self.mainString, color=bm.fg.rbg(255, 255, 255)).final()
                        #moving cursor left
                        sys.stdout.write(bm.move_cursor.LEFT(pos=1000))
                        # moving cursor up
                        sys.stdout.write(bm.move_cursor.UP(1))
                        # clear entire line
                        sys.stdout.write(bm.clear.line(2))
                        # write the new string
                        sys.stdout.write(self.input)
                        # flush
                        sys.stdout.flush()
                        if self.clear_line is False:
                            # moving cursor down
                            sys.stdout.write(bm.move_cursor.DOWN(1))
                            # clear entire line
                            sys.stdout.write(bm.clear.line(2))
                        else: self.clear_line = False
                        # movin cursor left
                        sys.stdout.write(bm.move_cursor.LEFT(1000))
                    else:
                        self.input = self.input[: self.length] + bm.init.bold+bm.fg.rbg(255, 255, 255)+self.mainString+bm.init.reset
                        # move cursor left
                        sys.stdout.write(bm.move_cursor.LEFT(pos=1000))
                        # clear entire line 
                        sys.stdout.write(bm.clear.line(2))
                        # write input 
                        sys.stdout.write(self.input)
                        # move left again 
                        sys.stdout.write(bm.move_cursor.LEFT(1000))
                        if self.clear_line is False: pass 
                        else:
                            # moving cursor up
                            sys.stdout.write(bm.move_cursor.UP(1))
                            # clear entire line 
                            sys.stdout.write(bm.clear.line(2))
                            # move cursor left
                            sys.stdout.write(bm.move_cursor.LEFT(1000))
                            # clear_line initialized to False
                            self.clear_line = False
                    ######################################################################
                    if self.mainString:
                        # running lexer 
                        self.lexer, self.normal_string, self.error = main.MAIN(self.mainString, self.data_base, self.line).MAIN()
                        if self.error is None :
                            if self.lexer is not None:
                                
                                # running parser 
                                self.num, self.key, self.error = parxer.ASSEMBLY(self.lexer, self.data_base,
                                        self.line).GLOBAL_ASSEMBLY(main_string=self.normal_string, interpreter = False, term=terminal_name)
                                if self.error is None: self.cursor.append(bm.get_cursor_pos.pos)   
                                else:
                                    sys.stdout.write(bm.clear.line(2))
                                    sys.stdout.write(bm.move_cursor.LEFT(1000))
                                    print('{}\n'.format(bm.init.bold+self.error))
                                    self.error = None
                            else:  pass
                        else:
                            sys.stdout.write(bm.clear.line(2))
                            sys.stdout.write(bm.move_cursor.LEFT(1000))
                            print('{}\n'.format(bm.init.bold+self.error))
                            self.error = None
                    else:  pass

                    # initialization 
                    self.input      = self.main_input
                    self.index      = self.length
                    self.key        = False
                    self.mainString = ''
                    self.mainIndex  = 0
                # tabular
                elif self.char == 9:  
                    self.tabular = '\t'
                    self.input = self.input[: self.index] + self.tabular + self.input[self.index:]
                    self.index += 1
                                        
                # moving cursor left
                sys.stdout.write(bm.move_cursor.LEFT(pos=1000))
                # clear line 
                sys.stdout.write(bm.clear.line(pos=0))
                # write string
                if terminal_name == "pegasus":
                    sys.stdout.write(bm.string().syntax_highlight(name=self.input))
                else: sys.stdout.write(self.main_input+bm.string().syntax_highlight( bm.words(string=self.mainString, color=bm.fg.white_L).final() ))
                # move cusor left again 
                sys.stdout.write(bm.move_cursor.LEFT(pos=1000))

                # updating cursor position on the line 
                if self.index > 0:  sys.stdout.write(bm.move_cursor.RIGHT(self.index - self.sub_length))
                else:   pass

                # flush
                sys.stdout.flush()
                   
            #keyboardInterrupt
            except KeyboardInterrupt:
                sys.stdout.write(bm.clear.screen(pos=1))
                sys.stdout.write(bm.cursorPos.to(0,0))
                sys.stdout.write(bm.clear.screen(pos=0))
                sys.stdout.write(bm.move_cursor.DOWN(pos=1))
                sys.stdout.write(bm.move_cursor.LEFT(pos=1000))
                sys.stdout.write(bm.clear.line(pos=0))
                self._keyboard_ = bm.bg.red_L + bm.fg.white_L + "KeyboardInterrupt" + bm.init.reset+bm.init.reset
                print(bm.init.bold+self._keyboard_)
                return
            # EOF
            except TypeError:
                self._end_of_file_ = bm.bg.red_L + bm.fg.white_L + "EOFError" + bm.init.reset+bm.init.reset
                print(bm.init.bold+self._end_of_file_)
                self.input = '{}>>> {}'.format(bm.fg.yellow_L, bm.init.reset)
                sys.stdout.write(bm.string().syntax_highlight(name=self.input))
                sys.stdout.flush()
                return

if __name__ == '__main__':

    term = 'orion'
    try:
        os.system('cls')
        sys.stdout.write(bm.save.save)
        if term == 'orion': header.header(terminal='orion terminal')
        else: header.header(terminal='pegasus terminal')
        
        data_base = db.DATA_BASE().STORAGE().copy()
        windows( data_base=data_base).terminal(c=bm.fg.rbg(255, 255, 255), terminal_name=term)
    except KeyboardInterrupt:  pass
    except IndexError: pass