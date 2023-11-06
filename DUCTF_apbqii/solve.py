K = 2^2000
n = 19604411241131769363446674414275822275458180476470552084588074159518829172495704100505151090666577360738167275118902368371310303168115405693118232835691333564186301532462296609038929723894816307213749698854885742811071911120730847279568876996811433319487396434622751326281226335521193361938724747445445693062336009352580319440819629260614301234971135026395941954109172567154559773437059174108362692061503832044135079892892132874437669744266153424229215832487832220575345912010076934611701182205068942016022731469408259665250938484104489962832891496953003599692437819685070043991828977623632396604764153766442526750861
c = 16285668872352205553535195410427806596787838055817589230402081772267074935944610262823936480340920868690431897597533868262062616060037808676539290467732178272289192993251540763800683055555842878669862850848141950704501553807462214356142018528608581546359772903806691435935873069006470208826518183488708349814610769150918356795466688732617809664831695402633481224388822180989614886783145141129157248734213457746877012517003702540070132542733288350979858743766340483503277308585752213220454288897741262154622769402029906981612699288206404870733274360554941455758083078106150045394190625280336371690998959720015636304971
hints = [773921762798470573303163880380136299117907456177270598418425239064611119645412840945432294881005107606154919094297188183879147500755682510817840590276985061404198538395146658442221987303866921786284298394947485319583779671756246394491275898343836522004269864718405399287554020900395899143149709408762450693357109188640512875099087677956684946219071353228860650842182953922400081939934842271539450654323, 1506346165967409413422972644306025635334450240732478358292064973873339506571546529986180145578525288707094235933775031106971678278204568310035260899591267480098015553318079460357474533531922997212816264042117005473870580122983241038123126855791876827449194400045937398578284016176289760858365282167537689282643483235235028505475719615108102516557986483184881658418430287064598580231630440534438966422546, 531028473288853560172466570664059891687387973059926255729701774553291285115938502989142318123512885100092638435578692032744904444237266108167428726130739434630511943317357743527053899234918340191006102436386051432760331852295930159729030763033361158582919982579082557775409422474301977588011705535991555292564664521116375190464371518812625647175447427886432255779925378071998411170643507118426289778768]
A = Matrix(QQ, nrows=6, ncols=6)
A[0, 0] = -hints[1]
A[0, 1] = hints[0]
A[1,1] = -hints[2]
A[1,2] = hints[1]
A[2,2] = -hints[0]
A[2,0] = hints[2]
A[3,0] = A[4,1] = A[5,2] = n
A *= K
A[0,3] = A[1,4] = A[2,5] = 1
p = gcd(A.LLL()[0,3], n)
q = n / p
print(int(pow(c, pow(0x10001, -1, (p-1)*(q-1)), n)).to_bytes(66, byteorder="big"))
