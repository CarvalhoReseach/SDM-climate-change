  #usual R libraries
  #=================================
  library(raster)
  library(sf)
  #=================================
  files<-list.files('/home/eduardo/projetos/conservacao_de_plantas_mudancas_climaticas/data/model_data/soil/world/',pattern='.tif')
  caatinga<-st_read("/home/eduardo/projetos/conservacao_de_plantas_mudancas_climaticas/data/shapes/caatinga_ibge_2019_escala250m/caatinga_250m_2019.shp")
  path<-paste('/home/eduardo/projetos/conservacao_de_plantas_mudancas_climaticas/data/model_data/soil/world/',files,sep='')
        
  for (i in 1:length(path)){
  fname<-paste('/home/eduardo/projetos/conservacao_de_plantas_mudancas_climaticas/data/model_data/soil/caatinga/caatinga_',files[i],sep='')
  raster_data<-raster(path[i])
  croped<-crop(raster_data,extent(caatinga))
  masked<-mask(croped,caatinga)
  print(path[i])
  plot(masked)
  writeRaster(masked, filename=fname, format="GTiff", overwrite=TRUE)
  }
        
  









  