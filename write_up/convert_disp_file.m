function ans = convert_disp_file( max_ribs, max_spars)

  disp_raw = dlmread( 'max_displacements.txt');

  [disp_x, disp_y] = size( disp_raw);
  if max_spars ~= disp_x || max_ribs ~= disp_y
    fprintf( 'Given max_spars and max_ribs do not match max_displacements size\n');
  end

  num_entries = max_ribs * max_spars;
  data = zeros( num_entries, 3);
  entry_number = 1;
  for s=1:max_spars
    for r = 1:max_ribs
      data(entry_number, 1) = s;
      data(entry_number, 2) = r;
      disp_ft = disp_raw( r,s);
      disp_m  = disp_ft * 0.3048;
      data(entry_number, 3) = disp_m;

      entry_number = entry_number + 1;
    end
  end

  tri = delaunay( data(:,1), data(:,2));
  dlmwrite('triangles.txt', tri-1, ' ');
  dlmwrite('surface_plot_data.txt', data, ' ');
end
