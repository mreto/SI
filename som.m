addpath ./somtoolbox
rehash toolboxcache
clear
clc


keywords = textread('./keywords_full', '%s');

## generate neutral map
sD = som_read_data('./data/basic_data/neutral_from_wiki.dat');
sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
sM = som_autolabel(sM,sD);
som_show(sM,'umat','all','empty','wszystkie');
som_show_add('label',sM,'TextSize',5,'subplot','all');
som_show(sM,'comp',18);
som_show_add('label',sM,'TextSize',5,'TextColor', 'w', 'subplot',1);
[neutral_unit_diffrence, neutral_l2_diffrence] = get_diffrences(sM, keywords);
last_unit_diffrence = neutral_unit_diffrence;
last_l2_diffrence = neutral_l2_diffrence;
print('./som_maps/basic_maps/neutral.jpg')



## generate biased catastrophy map
sD = som_read_data('./data/basic_data/correct_catastrophy.dat')
sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
sM = som_autolabel(sM,sD);
som_show(sM,'umat','all','empty','wszystkie');
som_show_add('label',sM,'TextSize',5,'subplot','all');
som_show(sM,'comp',18);
som_show_add('label',sM,'TextSize',5,'TextColor', 'w', 'subplot',1);
print('./som_maps/basic_maps/catastrophy.jpg')
[catastrophy_unit_diffrence, catastrophy_l2_diffrence] = get_diffrences(sM, keywords);


## generate biased assasination map
sD = som_read_data('./data/basic_data/correct_assasination.dat')
sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
sM = som_autolabel(sM,sD);
som_show(sM,'umat','all','empty','wszystkie');
som_show_add('label',sM,'TextSize',5,'subplot','all');
som_show(sM,'comp',18);
som_show_add('label',sM,'TextSize',5,'TextColor', 'w', 'subplot',1);
print('./som_maps/basic_maps/catastrophy.jpg')
[assasination_unit_diffrence, assasination_l2_diffrence] = get_diffrences(sM, keywords);



files_x = cell
files_x{1} = ('./data/basic_data/correct_catastrophy.dat');
files_x{2} = ('./data/basic_data/neutral_from_wiki.dat');
files_x{3} = ('./data/basic_data/correct_assasination.dat');
files_x{4} = ('./data/basic_data/neutral_from_wiki.dat');
compareFiles(files_x,files_x, 'numerical_compare/basic_comparison.csv');
files_catastrophy = glob('./data/single_articles_data/catastrophy/*');
compareFiles(files_catastrophy,files_x, 'numerical_compare/single_articles_catastrophy.csv');

files_assasination = glob('./data/single_articles_data/assasination/*');
compareFiles(files_assasination,files_x, 'numerical_compare/single_articles_assasination.csv');



files = glob('./data/biased_catastrophy/part/*')
diffrences = cell(numel(files), 9)
for i=1:numel(files)
  [~, name] = fileparts (files{i});
  full_name = ['./som_maps/biased_catastrophy_part/', name, '.jpg']
  dir_data = files{i};
  sD = som_read_data(dir_data);
  sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
  sM = som_autolabel(sM,sD);
  [current_unit_diffrence, current_l2_diffrence] = get_diffrences(sM, keywords);
  diffrences(i, 1) = comp_diffrence(current_unit_diffrence, neutral_unit_diffrence);
  diffrences(i, 2) = comp_diffrence(current_unit_diffrence, catastrophy_unit_diffrence);
  diffrences(i, 3) = comp_diffrence(current_unit_diffrence, assasination_unit_diffrence);
  diffrences(i, 4) = comp_diffrence(current_unit_diffrence, last_unit_diffrence);
  diffrences(i, 5) = comp_diffrence(current_l2_diffrence, neutral_l2_diffrence);
  diffrences(i, 6) = comp_diffrence(current_l2_diffrence, catastrophy_l2_diffrence);
  diffrences(i, 7) = comp_diffrence(current_l2_diffrence, assasination_l2_diffrence);
  diffrences(i, 8) = comp_diffrence(current_l2_diffrence, last_l2_diffrence);
  diffrences(i, 9) = name;
  last_unit_diffrence = current_unit_diffrence;
  last_l2_diffrence = current_l2_diffrence;
  som_show(sM,'umat','all','empty','wszystkie');
  som_show_add('label',sM,'TextSize',5,'subplot','all');
  som_show(sM,'comp',18);
  som_show_add('label',sM,'TextSize',5,'TextColor', 'w', 'subplot',1);
  print(full_name)
endfor
fid = fopen('./numerical_compare/catastrophy_part.csv', 'w')
fprintf(fid, 'neutral_unit, catastrophy_unit, assasination_unit last_unit, neutral_l2, catastrophy_l2, assasination_l2, last_l2 \n');
for i=1:numel(files)
  fprintf(fid, '%s, ', diffrences{i,9}) ;
  fprintf(fid, '%f, ', diffrences{i,1:7}) ;
  fprintf(fid, '\n') ;
endfor
fclose(fid) ;




files = glob('./data/biased_catastrophy/multiply/*')
diffrences = cell(numel(files), 7)
for i=1:numel(files)
  [~, name] = fileparts (files{i});
  dir_data = files{i};
  full_name = ['./som_maps/biased_catastrophy_multiply', name, '.jpg']
  sD = som_read_data(dir_data);
  sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
  sM = som_autolabel(sM,sD);
  [current_unit_diffrence, current_l2_diffrence] = get_diffrences(sM, keywords);
  diffrences(i, 1) = comp_diffrence(current_unit_diffrence, neutral_unit_diffrence);
  diffrences(i, 2) = comp_diffrence(current_unit_diffrence, catastrophy_unit_diffrence);
  diffrences(i, 3) = comp_diffrence(current_unit_diffrence, assasination_unit_diffrence);
  diffrences(i, 4) = comp_diffrence(current_unit_diffrence, last_unit_diffrence);
  diffrences(i, 5) = comp_diffrence(current_l2_diffrence, neutral_l2_diffrence);
  diffrences(i, 6) = comp_diffrence(current_l2_diffrence, catastrophy_l2_diffrence);
  diffrences(i, 7) = comp_diffrence(current_l2_diffrence, assasination_l2_diffrence);
  diffrences(i, 8) = comp_diffrence(current_l2_diffrence, last_l2_diffrence);
  diffrences(i, 9) = name;
  last_unit_diffrence = current_unit_diffrence;
  last_l2_diffrence = current_l2_diffrence;
  som_show(sM,'umat','all','empty','wszystkie');
  som_show_add('label',sM,'TextSize',5,'subplot','all');
  som_show(sM,'comp',18);
  som_show_add('label',sM,'TextSize',5,'TextColor', 'w', 'subplot',1);
  print(full_name)
endfor
fid = fopen('./numerical_compare/catastrophy_multiply.csv', 'w')
fprintf(fid, 'neutral_unit, catastrophy_unit, assasination_unit last_unit, neutral_l2, catastrophy_l2, assasination_l2, last_l2 \n');
for i=1:numel(files)
  fprintf(fid, '%s, ', diffrences{i,9}) ;
  fprintf(fid, '%f, ', diffrences{i,1:7}) ;
  fprintf(fid, '\n') ;
endfor
fclose(fid) ;

























files = glob('./data/biased_assasination/part/*')
diffrences = cell(numel(files), 7)
for i=1:numel(files)
  [~, name] = fileparts (files{i});
  dir_data = files{i};
  full_name = ['./som_maps/biased_assasination_part/', name, '.jpg']
  sD = som_read_data(dir_data);
  sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
  sM = som_autolabel(sM,sD);
  [current_unit_diffrence, current_l2_diffrence] = get_diffrences(sM, keywords);
  diffrences(i, 1) = comp_diffrence(current_unit_diffrence, neutral_unit_diffrence);
  diffrences(i, 2) = comp_diffrence(current_unit_diffrence, catastrophy_unit_diffrence);
  diffrences(i, 3) = comp_diffrence(current_unit_diffrence, assasination_unit_diffrence);
  diffrences(i, 4) = comp_diffrence(current_unit_diffrence, last_unit_diffrence);
  diffrences(i, 5) = comp_diffrence(current_l2_diffrence, neutral_l2_diffrence);
  diffrences(i, 6) = comp_diffrence(current_l2_diffrence, catastrophy_l2_diffrence);
  diffrences(i, 7) = comp_diffrence(current_l2_diffrence, assasination_l2_diffrence);
  diffrences(i, 8) = comp_diffrence(current_l2_diffrence, last_l2_diffrence);
  diffrences(i, 9) = name;
  last_unit_diffrence = current_unit_diffrence;
  last_l2_diffrence = current_l2_diffrence;
  som_show(sM,'umat','all','empty','wszystkie');
  som_show_add('label',sM,'TextSize',5,'subplot','all');
  som_show(sM,'comp',18);
  som_show_add('label',sM,'TextSize',5,'TextColor', 'w', 'subplot',1);
  print(full_name)
endfor
fid = fopen('./numerical_compare/assasination_part.csv', 'w')
fprintf(fid, 'neutral_unit, catastrophy_unit, assasination_unit last_unit, neutral_l2, catastrophy_l2, assasination_l2, last_l2 \n');
for i=1:numel(files)
  fprintf(fid, '%s, ', diffrences{i,9}) ;
  fprintf(fid, '%f, ', diffrences{i,1:7}) ;
  fprintf(fid, '\n') ;
endfor
fclose(fid) ;




files = glob('./data/biased_assasination/multiply/*')
diffrences = cell(numel(files), 7)
for i=1:numel(files)
  [~, name] = fileparts (files{i});
  dir_data = files{i};
  full_name = ['./som_maps/biased_assasination_multiply/', name, '.jpg']
  sD = som_read_data(dir_data);
  sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
  sM = som_autolabel(sM,sD);
  [current_unit_diffrence, current_l2_diffrence] = get_diffrences(sM, keywords);
  diffrences(i, 1) = comp_diffrence(current_unit_diffrence, neutral_unit_diffrence);
  diffrences(i, 2) = comp_diffrence(current_unit_diffrence, catastrophy_unit_diffrence);
  diffrences(i, 3) = comp_diffrence(current_unit_diffrence, assasination_unit_diffrence);
  diffrences(i, 4) = comp_diffrence(current_unit_diffrence, last_unit_diffrence);
  diffrences(i, 5) = comp_diffrence(current_l2_diffrence, neutral_l2_diffrence);
  diffrences(i, 6) = comp_diffrence(current_l2_diffrence, catastrophy_l2_diffrence);
  diffrences(i, 7) = comp_diffrence(current_l2_diffrence, assasination_l2_diffrence);
  diffrences(i, 8) = comp_diffrence(current_l2_diffrence, last_l2_diffrence);
  diffrences(i, 9) = name;
  last_unit_diffrence = current_unit_diffrence;
  last_l2_diffrence = current_l2_diffrence;
  som_show(sM,'umat','all','empty','wszystkie');
  som_show_add('label',sM,'TextSize',5,'subplot','all');
  som_show(sM,'comp',18);
  som_show_add('label',sM,'TextSize',5,'TextColor', 'w', 'subplot',1);
  print(full_name)
endfor
fid = fopen('./numerical_compare/assasination_multiply.csv', 'w')
fprintf(fid, 'neutral_unit, catastrophy_unit, assasination_unit last_unit, neutral_l2, catastrophy_l2, assasination_l2, last_l2 \n');
for i=1:numel(files)
  fprintf(fid, '%s, ', diffrences{i,9}) ;
  fprintf(fid, '%f, ', diffrences{i,1:7}) ;
  fprintf(fid, '\n') ;
endfor
fclose(fid) ;
