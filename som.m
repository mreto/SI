addpath ./somtoolbox
rehash toolboxcache
clear
clc


keywords = textread('./keywords_full', '%s');

## generate neutral map
sD = som_read_data('./data/new_generated_data/neutral_from_wiki.dat');
sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
sM = som_autolabel(sM,sD);
som_show(sM,'umat','all','empty','wszystkie');
som_show_add('label',sM,'TextSize',5,'subplot','all');
som_show(sM,'comp',18);
som_show_add('label',sM,'TextSize',5,'TextColor', 'w', 'subplot',1);
[neutral_unit_diffrence, neutral_l2_diffrence] = get_diffrences(sM, keywords);
last_unit_diffrence = neutral_unit_diffrence;
last_l2_diffrence = neutral_l2_diffrence;
print('./som_maps/basic_maps/neutral.pdf')



## generate biased catastrophy map
sD = som_read_data('data/new_generated_data/correct_catastrophy.dat');
sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
sM = som_autolabel(sM,sD);
som_show(sM,'umat','all','empty','wszystkie');
som_show_add('label',sM,'TextSize',5,'subplot','all');
som_show(sM,'comp',18);
som_show_add('label',sM,'TextSize',5,'TextColor', 'w', 'subplot',1);
print('./som_maps/basic_maps/catastrophy.pdf')
[catastrophy_unit_diffrence, catastrophy_l2_diffrence] = get_diffrences(sM, keywords);



files = glob('./data/biased_catastrophy/neutral_plus_part_catastrophy/*')

diffrences = cell(numel(files), 7)
for i=1:numel(files)
  [~, name] = fileparts (files{i});
  full_name = ['./som_maps/biased_catastrophy_multiply/', name, '.pdf']
  dir_data = files{i};
  sD = som_read_data(dir_data);
  sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
  sM = som_autolabel(sM,sD);
  [current_unit_diffrence, current_l2_diffrence] = get_diffrences(sM, keywords);
  diffrences(i, 1) = comp_diffrence(current_unit_diffrence, neutral_unit_diffrence);
  diffrences(i, 2) = comp_diffrence(current_unit_diffrence, catastrophy_unit_diffrence);
  diffrences(i, 3) = comp_diffrence(current_unit_diffrence, last_unit_diffrence);
  diffrences(i, 4) = comp_diffrence(current_l2_diffrence, neutral_l2_diffrence);
  diffrences(i, 5) = comp_diffrence(current_l2_diffrence, catastrophy_l2_diffrence);
  diffrences(i, 6) = comp_diffrence(current_l2_diffrence, last_l2_diffrence);
  diffrences(i, 7) = name;
  last_unit_diffrence = current_unit_diffrence;
  last_l2_diffrence = current_l2_diffrence;
  som_show(sM,'umat','all','empty','wszystkie');
  som_show_add('label',sM,'TextSize',5,'subplot','all');
  som_show(sM,'comp',18);
  som_show_add('label',sM,'TextSize',5,'TextColor', 'w', 'subplot',1);
  print(full_name)
endfor

fid = fopen('./som_maps/biased_catastrophy_multiply/diffrences.csv', 'w')
fprintf(fid, 'filename, neutral-current_unit, biased-neutral_unit, last-neutral_unit, neutral-current_l2, biased-current_l2, last-current_l2 \n');
for i=1:numel(files)
  fprintf(fid, '%s, ', diffrences{i,7}) ;
  fprintf(fid, '%f, ', diffrences{i,1:6}) ;
  fprintf(fid, '\n') ;
endfor
fclose(fid) ;




files = glob('./data/biased_catastrophy/neutral_plus_part_catastrophy/*')

diffrences = cell(numel(files), 7)
for i=1:numel(files)
  [~, name] = fileparts (files{i});
  dir_data = files{i};
  full_name = ['./som_maps/biased_catastrophy_part/', name, '.pdf']
  sD = som_read_data(dir_data);
  sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
  sM = som_autolabel(sM,sD);
  [current_unit_diffrence, current_l2_diffrence] = get_diffrences(sM, keywords);
  diffrences(i, 1) = comp_diffrence(current_unit_diffrence, neutral_unit_diffrence);
  diffrences(i, 2) = comp_diffrence(current_unit_diffrence, catastrophy_unit_diffrence);
  diffrences(i, 3) = comp_diffrence(current_unit_diffrence, last_unit_diffrence);
  diffrences(i, 4) = comp_diffrence(current_l2_diffrence, neutral_l2_diffrence);
  diffrences(i, 5) = comp_diffrence(current_l2_diffrence, catastrophy_l2_diffrence);
  diffrences(i, 6) = comp_diffrence(current_l2_diffrence, last_l2_diffrence);
  diffrences(i, 7) = name;
  last_unit_diffrence = current_unit_diffrence;
  last_l2_diffrence = current_l2_diffrence;
  som_show(sM,'umat','all','empty','wszystkie');
  som_show_add('label',sM,'TextSize',5,'subplot','all');
  som_show(sM,'comp',18);
  som_show_add('label',sM,'TextSize',5,'TextColor', 'w', 'subplot',1);
  print(full_name)
endfor

fid = fopen('./som_maps/biased_catastrophy_part/diffrences.csv', 'w')
fprintf(fid, 'filename, neutral-current_unit, biased-neutral_unit, last-neutral_unit, neutral-current_l2, biased-current_l2, last-current_l2 \n');
for i=1:numel(files)
  fprintf(fid, '%s, ', diffrences{i,7}) ;
  fprintf(fid, '%f, ', diffrences{i,1:6}) ;
  fprintf(fid, '\n') ;
endfor
fclose(fid) ;
