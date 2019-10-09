

"""
    Print layout 

    Big Text 
    Normal text 
        
        Left align 
        Center align 
    
    Image printing to the center only 
    Space / margin 
    

    >>> from escpos.printer import Usb
    >>> cp = Usb(0x4b43, 0x3538, 0, out_ep=0x02)
    >>> cp.text("hi there \n")
    >>> cp.cut()


"""

# from escpos.printer import Usb

# """ Seiko Epson Corp. Receipt Printer (EPSON TM-T88III) """
# p = Usb(0x04b8, 0x0202, 0, profile="TM-T88III")
# p.text("Hello World\n")
# p.image("logo.gif")
# p.barcode('1324354657687', 'EAN13', 64, 2, '', '')
# p.cut()




PARTIAL_CUT = b'\x1dV\x01'
FULL_CUT = b'\x1dV\x00'

TXT_NORMAL     = ESC + b'!\x00'     # Normal text
TXT_2HEIGHT    = ESC + b'!\x10'     # Double height text
TXT_2WIDTH     = ESC + b'!\x20'     # Double width text
TXT_4SQUARE    = ESC + b'!\x30'     # Quad area text
TXT_UNDERL_OFF = ESC + b'\x2d\x00'  # Underline font OFF
TXT_UNDERL_ON  = ESC + b'\x2d\x01'  # Underline font 1-dot ON
TXT_UNDERL2_ON = ESC + b'\x2d\x02'  # Underline font 2-dot ON
TXT_BOLD_OFF   = ESC + b'\x45\x00'  # Bold font OFF
TXT_BOLD_ON    = ESC + b'\x45\x01'  # Bold font ON
TXT_FONT_A     = ESC + b'\x4d\x00'  # Font type A
TXT_FONT_B     = ESC + b'\x4d\x01'  # Font type B
TXT_ALIGN_LT   = ESC + b'\x61\x00'  # Left justification
TXT_ALIGN_CT   = ESC + b'\x61\x01'  # Centering
TXT_ALIGN_RT   = ESC + b'\x61\x02'  # Right justification


LINESPACING_RESET = ESC + b'2'
LINESPACING_FUNCS = {
  60: ESC + b'A',  # line_spacing/60 of an inch, 0 <= line_spacing <= 85
  360: ESC + b'+', # line_spacing/360 of an inch, 0 <= line_spacing <= 255
  180: ESC + b'3', # line_spacing/180 of an inch, 0 <= line_spacing <= 255
}



["hi there", '\n\r', "items for purhcase", '\n\r', 
 "i hope this meeets the condition", '']

class PrintLib:

    def __init__(self):
        pass





