function [out] = compareFiles(f1, f2, print_file)
  ## compare every file in f1 with every file in f2. Returns matrix f1.dim x f2.dim with values of diffrences
  addpath ./somtoolbox
  rehash toolboxcache
  
  

  keywords = textread('./keywords_full', '%s');
  [key_dim, _ ]= size(keywords);
  d1 = cell 
  numel(f1)
  for i=1:numel(f1)
    f1{i}
    sD = som_read_data(f1{i});
    sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
    sM = som_autolabel(sM,sD);
    [unit_diffrence, l2_diffrence] = get_diffrences(sM, keywords);
    d1(i, 1) = unit_diffrence;
    d1(i, 2) = l2_diffrence;
  endfor
  d2 = cell
  for i=1:numel(f2)
    sD = som_read_data(f2{i});
    sM = som_make(sD, 'msize', [12, 12], 'lattice', 'hexa');
    sM = som_autolabel(sM,sD);
    [unit_diffrence, l2_diffrence] = get_diffrences(sM, keywords);
    d2(i, 1) = unit_diffrence;
    d2(i, 2) = l2_diffrence;
  endfor


  out = cell

  for i=1:numel(f1)
    for j=1:numel(f2)
      out{i, j} = comp_diffrence(d1{i, 1}, d2{j, 1});
    endfor
  endfor


  fid = fopen(print_file, 'w')
  for i=1:numel(f2)
    [~, name] = fileparts (f2{i});
    fprintf(fid, '%s, ', name);
  endfor
  fprintf(fid, '\n');
  for i=1:numel(f1)
    [~, name] = fileparts (f1{i});
    fprintf(fid, '%s, ', name);
    fprintf(fid, '%f, ', out{i,1:end}) ;
    fprintf(fid, '\n') ;
  endfor
  fclose(fid);
end
