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
description(alpine, 'World Championships: 2').
description(alpine, 'Pole Positions: 20').
description(alpine, 'https://www.formula1.com/en/teams/alpine').
description(alpine, 'https://www.alpinecars.es/formula-1.html').

description(astonmartin, 'A relatively new brand with significant ambitions.').
description(astonmartin, 'Backed by a luxurious and prestigious image.').
description(astonmartin, 'Pole Positions: 1').
description(astonmartin, 'https://www.formula1.com/en/teams/aston-martin').
description(astonmartin, 'https://www.astonmartinf1.com/').

description(ferrari, 'The most iconic and historic team in Formula 1.').
description(ferrari, 'World Championships: 16".').
description(ferrari, 'Pole Positions: 253').
description(ferrari, 'https://www.formula1.com/en/teams/ferrari').
description(ferrari, 'https://www.ferrari.com/en-EN/formula1').

description(haas, 'The only American team on the grid.').
description(haas, 'Relies on a partnership with Ferrari for engine supply.').
description(haas, 'Pole Positions: 1').
description(haas, 'https://www.formula1.com/en/teams/haas').
description(haas, 'https://www.haasf1team.com/').

description(kick, 'Historically significant, with roots dating back to F1’s inception.').
description(kick, 'Partners with Sauber for operations and development.').
description(kick, 'Often competes at the lower end of the midfield.').
description(kick, 'Pole Positions: 1').
description(kick, 'https://www.formula1.com/en/teams/kick-sauber').

description(mclaren, 'Boasts a rich history of championship wins.').
description(mclaren, 'World Championships: 9').
description(mclaren, 'Pole positions: 164').
description(mclaren, 'https://www.formula1.com/en/teams/mclaren').
description(mclaren, 'https://cars.mclaren.com/es-es/legacy/mclaren-f1').

description(mercedes, 'Known for its consistent performance and technical innovation.').
description(mercedes, 'World Championships: 8').
description(mercedes, 'Pole Positions: 133').
description(mercedes, 'https://www.formula1.com/en/teams/mercedes').
description(mercedes, 'https://www.mercedesamgf1.com/').

description(rb, 'Serves as Red Bulls junior team.').
description(rb, 'A testing ground for upcoming driver talent.').
description(rb, 'Pole Positions: 1').
description(rb, 'https://www.formula1.com/en/teams/racing-bulls').
description(rb, 'https://www.visacashapprb.com/int-en').

description(redbull, 'Renowned for its aggressive race strategies.').
description(redbull, 'World Championships: 6').
description(redbull, 'Pole Positions: 103').
description(redbull, 'https://www.formula1.com/en/teams/red-bull-racing').
description(redbull, 'https://www.redbull.com/ar-es/tags/f1').

description(williams, 'A legendary team with a history of numerous championships.').
description(williams, 'World Championships: 9').
description(williams, 'Pole Positions: 128').
description(williams, 'https://www.formula1.com/en/teams/williams').
description(williams, 'https://www.williamsf1.com/').

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