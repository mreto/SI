## addpath ./somtoolbox
## rehash toolboxcache
## clear
## clc

## ## sD = som_read_data('new_generated_data/correct_articles.dat');
## ## sD = som_read_data('new_generated_data/correct_assasination.dat');
## sD = som_read_data('output/output1.dat');

## %sD = som_read_data('old_generated_data/articles_values.dat');
## %sD = som_read_data('old_generated_data/assasination_frequencies.dat');
## %sD = som_read_data('old_generated_data/assasination_values.dat');
## %sD = som_read_data('old_generated_data/catastrophy_frequencies.dat');
## %sD = som_read_data('old_generated_data/catastrophy_values.dat');

## sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
## sM = som_autolabel(sM,sD);
## som_show(sM,'umat','all','empty','wszystkie');
## som_show_add('label',sM,'TextSize',8,'subplot','all');
## som_show(sM,'comp',18);
## som_show_add('label',sM,'TextSize',8,'TextColor', 'w', 'subplot',1);
## print img.pdf



addpath ./somtoolbox
rehash toolboxcache
files = glob('output/*')
kk = genpath ('output/')
for i=1:numel(files)
  [~, name] = fileparts (files{i});
  full_name = ['./output_inne_kolory/', name, '.pdf']
  dir_data = files{i}
  rehash toolboxcache
  clear sD
  clear sM
  clc
  dir_data
  ## sD = som_read_data(eval(sprintf('%s = load("%s", "-ascii");', name, files{i})));
  sD = som_read_data(dir_data);
  sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
  sM = som_autolabel(sM,sD);
  som_show(sM,'umat','all','empty','wszystkie');
  som_show_add('label',sM,'TextSize',8,'subplot','all');
  som_show(sM,'comp',18);
  som_show_add('label',sM,'TextSize',8,'TextColor', 'w', 'subplot',1);
  print(full_name)
endfor
