function [diff] = comp_diffrence(m1, m2)
  diff = m1-m2;
  diff = sum(diff(:));
end
