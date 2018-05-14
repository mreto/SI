function [unit_diffrences, mutal_diffrences] = get_diffrences(sM, keywords)
  ## returns the matrix, sized keyword_dim x keyword_dim, with distance or L2 norm from two keywords on som map

  addpath ./somtoolbox
  rehash toolboxcache

  [key_dim, _ ]= size(keywords);

  ## array with coordiates of all keywords;
  coordinates = zeros(key_dim);
  labels = sM.labels;

  ## assign every keyword matching coordianates from labels
  [dim1, dim2] = size(labels);
  for i = 1:dim1
    for j = 1:dim2
      if (!strcmp (labels{i, j},""))
        for key_id = 1:key_dim
          keywords{key_id, 1};
          labels{i, j};
          if (strcmp (labels{i, j},keywords{key_id, 1}));
            coordinates(key_id) = i;
          endif
        endfor
      endif
    endfor
  endfor

  ## unit_dist is distance on board from two points
  unit_dist = som_unit_dists(sM.topol);
  ## mutal_dist is L2 norm from two vectors at specific points
  mutal_dist = som_mdist(sM);

  unit_diffrences = zeros(key_dim, key_dim);
  mutal_diffrences = zeros(key_dim, key_dim);

  ## count diffrence for every keyword and put it to matrix key_dim x key_dim
  for i = 1:key_dim
    for j = 1:key_dim
      unit_diffrences(i, j) = unit_dist(coordinates(i), coordinates(j));
      mutal_diffrences(i, j) = mutal_dist(coordinates(i), coordinates(j));
    endfor
  endfor
end
