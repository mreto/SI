addpath ./somtoolbox
rehash toolboxcache
clear
clc

## sD = som_read_data('new_generated_data/correct_articles.dat');
## sD = som_read_data('new_generated_data/correct_assasination.dat');
sD = som_read_data('new_generated_data/correct_catastrophy.dat');

%sD = som_read_data('old_generated_data/articles_values.dat');
%sD = som_read_data('old_generated_data/assasination_frequencies.dat');
%sD = som_read_data('old_generated_data/assasination_values.dat');
%sD = som_read_data('old_generated_data/catastrophy_frequencies.dat');
%sD = som_read_data('old_generated_data/catastrophy_values.dat');

sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
sM = som_autolabel(sM,sD);
som_show(sM,'umat','all','empty','wszystkie');
som_show_add('label',sM,'TextSize',8,'subplot','all');
som_show(sM,'comp',18);
som_show_add('label',sM,'TextSize',8,'TextColor', 'w', 'subplot',1);
