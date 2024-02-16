from config import print_stuff, config

# Setup print stuff from config class print_stuff
print_whitespace = print_stuff.printWhitespace
print_stars = print_stuff().printStars
string_stars = print_stuff().stringStars
print_stars_reset = print_stuff(reset=1).printStars
string_stars_reset = print_stuff(reset=1).stringStars

def parse_flags(parser, region, network):
    # Add the arguments
    parser.add_argument(
        "-u",
        "--update",
        action="store_true",
        help="Will update and/or restart your SERV Node.",
    )

    parser.add_argument(
        "-s",
        "--stats",
        action="store_true",
        help="Run your stats if SERV is installed and running.",
    )

    parser.add_argument(
        "-c",
        "--claim",
        action="store_true",
        help="Claim all of your pending Unclaimed SERV.",
    )

    parser.add_argument(
        "--installer",
        action="store_true",
        help="Will run the toolbox installer setup for mainnet or testnet.",
    )

    parser.add_argument(
        "--register",
        action="store_true",
        help="Will register your validator on chain after server is synced and deposit is made.",
    )

    # parse the arguments
    args = parser.parse_args()

    # Add other args here
    if args.claim:
        # We'll do something here soon!
        finish_node()
        
# loader intro splash screen
def loader_intro():
    print_stars()
    p = """*
*
* ███████╗███████╗██████╗ ██╗   ██╗                           
* ██╔════╝██╔════╝██╔══██╗██║   ██║                           
* ███████╗█████╗  ██████╔╝██║   ██║                           
* ╚════██║██╔══╝  ██╔══██╗╚██╗ ██╔╝                           
* ███████║███████╗██║  ██║ ╚████╔╝                            
* ╚══════╝╚══════╝╚═╝  ╚═╝  ╚═══╝                             
*                                                             
* ████████╗ ██████╗  ██████╗ ██╗     ██████╗  ██████╗ ██╗  ██╗
* ╚══██╔══╝██╔═══██╗██╔═══██╗██║     ██╔══██╗██╔═══██╗╚██╗██╔╝
*    ██║   ██║   ██║██║   ██║██║     ██████╔╝██║   ██║ ╚███╔╝ 
*    ██║   ██║   ██║██║   ██║██║     ██╔══██╗██║   ██║ ██╔██╗ 
*    ██║   ╚██████╔╝╚██████╔╝███████╗██████╔╝╚██████╔╝██╔╝ ██╗
*    ╚═╝    ╚═════╝  ╚═════╝ ╚══════╝╚═════╝  ╚═════╝ ╚═╝  ╚═╝
*
*     SERV Node Management
*     created by Patrick @ https://EasyNode.pro
*
*"""
    print(p)
    return

def finish_node() -> None:
    print_stars()
    print("Goodbye!")
    print_stars()
    return