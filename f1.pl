teams(mclaren, 'McLaren').
teams(ferrari, 'Ferrari').
teams(redbull, 'Red Bull Racing').
teams(mercedes, 'Mercedes').
teams(astonmartin, 'Aston Martin').
teams(alpine, 'Alpine').
teams(haas, 'Haas').
teams(rb, 'RB').
teams(williams, 'Williams').
teams(kick, 'Kick Sauber').

type(time).
type(color).
type(character).
type(football).
type(music).
type(crash).
type(number).

question(time, 'Hace cuanto tiempo ves Formula 1?').
question(color, 'Cual es tu color favorito?').
question(character, 'Elegi un personaje:').
question(football, 'De que equipo de futbol argentino sos?').
question(music, 'Que estilo de musica escuchas?').
question(crash, 'Cuantas veces chocaste el auto?').
question(number, 'Elegi un numero:').

time(mclaren, '2019 o antes').
time(ferrari, 'Arranque esta temporada').
time(redbull, 'Empece en la pandemia').
time(mercedes, 'Empece en la pandemia').
time(astonmartin, 'Nunca vi Formula 1').
time(alpine, '2019 o antes').
time(haas, 'Nunca vi Formula 1').
time(rb, 'Nunca vi Formula 1').
time(williams, 'Desde que llego Colapinto').
time(kick, 'Nunca vi Formula 1').

color(mclaren, 'naranja').
color(ferrari, 'rojo').
color(mercedes, 'verde agua').
color(astonmartin, 'verde').
color(kick, 'verde').
color(williams, 'azul').
color(rb, 'azul').
color(haas, 'negro').
color(redbull, 'otro').
color(alpine, 'otro').

character(redbull, 'assets/images/characters/mcqueen.png').
character(mclaren, 'assets/images/characters/mcqueen.png').
character(kick, 'assets/images/characters/mate.png').
character(alpine, 'assets/images/characters/sally.png').
character(mercedes, 'assets/images/characters/sally.png').
character(williams, 'assets/images/characters/dochudson.png').
character(astonmartin, 'assets/images/characters/dochudson.png').
character(rb, 'assets/images/characters/mack.png').
character(ferrari, 'assets/images/characters/guido.png').
character(haas, 'assets/images/characters/storm.png').

football(redbull, 'No miro futbol').
football(mercedes, 'No miro futbol').
football(mclaren, 'Boca').
football(ferrari, 'River').
football(williams, 'Independiente').
football(alpine, 'Racing').
football(astonmartin, 'Racing').
football(rb, 'Otro').
football(haas, 'Otro').
football(kick, 'Otro').

music(redbull, 'Electronica').
music(rb, 'Electronica').
music(astonmartin, 'Rock').
music(mclaren, 'Rock').
music(haas, 'Rock nacional').
music(mercedes, 'Musica clasica').
music(williams, 'Musica clasica').
music(ferrari, 'Baladas').
music(kick, 'Cachengue').
music(alpine, 'Cachengue').

crash(williams, '3 o mas veces').
crash(redbull, '3 o mas veces').
crash(ferrari, '2 veces en menos de un año').
crash(mercedes, '2 veces en menos de un año').
crash(astonmartin, '2 veces').
crash(rb, '2 veces').
crash(haas, '1 vez').
crash(kick, '1 vez').
crash(alpine, 'Nunca').
crash(mclaren, 'Nunca').

number(mercedes, '44').
number(redbull, '33').
number(ferrari, '16').
number(astonmartin, '14').
number(alpine, '31').
number(williams, '43').
number(kick, '77').
number(rb, '10').
number(haas, '22').
number(mclaren, '4').

description(alpine, 'Formerly known as Renault, representing French excellence.').
description(alpine, 'Focuses on strategic long-term development.').
description(alpine, 'Often a strong performer in midfield battles.').
description(alpine, 'Prioritizes developing their engine technology.').
description(alpine, 'Represents a bold brand identity in Formula 1.').

description(astonmartin, 'A relatively new brand with significant ambitions.').
description(astonmartin, 'Backed by a luxurious and prestigious image.').
description(astonmartin, 'Focuses on steady growth and securing sponsorships.').
description(astonmartin, 'Aims to attract top-tier drivers and engineers.').
description(astonmartin, 'Often competes as a challenger in the midfield.').

description(ferrari, 'The most iconic and historic team in Formula 1.').
description(ferrari, 'Passionate fanbase often referred to as the "Tifosi".').
description(ferrari, 'Focused on producing both chassis and power units in-house.').
description(ferrari, 'Known for emotional highs and lows in performance.').
description(ferrari, 'Aims to balance tradition with modern technology.').

description(haas, 'The only American team on the grid.').
description(haas, 'Relies on a partnership with Ferrari for engine supply.').
description(haas, 'Operates with a cost-effective strategy.').
description(haas, 'Frequently fluctuates in competitiveness.').
description(haas, 'Targets consistent points finishes as a primary goal.').

description(kick, 'Historically significant, with roots dating back to F1’s inception.').
description(kick, 'Partners with Sauber for operations and development.').
description(kick, 'Balances tradition with modern racing ambitions.').
description(kick, 'Known for nurturing young driver talent.').
description(kick, 'Often competes at the lower end of the midfield.').

description(mclaren, 'Boasts a rich history of championship wins.').
description(mclaren, 'Recently re-emerged as a strong contender in the midfield.').
description(mclaren, 'Invests heavily in young driver talent.').
description(mclaren, 'Known for innovation in car design and technology.').
description(mclaren, 'Engages fans with a vibrant and modern team image.').

description(mercedes, 'Known for its consistent performance and technical innovation.').
description(mercedes, 'Dominated the sport during the hybrid era.').
description(mercedes, 'Strong teamwork between drivers and engineers.').
description(mercedes, 'Focuses heavily on aerodynamics and power unit efficiency.').
description(mercedes, 'Often considered a benchmark for other teams.').

description(rb, 'Serves as Red Bull’s junior team.').
description(rb, 'A testing ground for upcoming driver talent.').
description(rb, 'Shares technical resources with Red Bull Racing.').
description(rb, 'Operates with a focus on development over results.').
description(rb, 'Represents a unique blend of performance and style.').

description(redbull, 'Renowned for its aggressive race strategies.').
description(redbull, 'Emphasizes a strong aerodynamic package.').
description(redbull, 'Consistently competes at the front of the grid.').
description(redbull, 'Fosters a competitive driver environment.').
description(redbull, 'Dominates circuits requiring high-speed cornering.').

description(williams, 'A legendary team with a history of numerous championships.').
description(williams, 'Currently undergoing a period of rebuilding and growth.').
description(williams, 'Focuses on maximizing results with limited resources.').
description(williams, 'Renowned for its independent and family-oriented heritage.').
description(williams, 'Aims to return to its former glory as a top team.').

image(alpine, 'assets/images/f1-teams/alpine.png').
image(astonmartin, 'assets/images/f1-teams/astonmartin.png').
image(ferrari, 'assets/images/f1-teams/ferrari.png').
image(haas, 'assets/images/f1-teams/haas.png').
image(kick, 'assets/images/f1-teams/kick.png').
image(mclaren, 'assets/images/f1-teams/mclaren.png').
image(mercedes, 'assets/images/f1-teams/mercedes.png').
image(rb, 'assets/images/f1-teams/rb.png').
image(redbull, 'assets/images/f1-teams/redbull.png').
image(williams, 'assets/images/f1-teams/williams.png').