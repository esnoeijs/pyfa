import threading
import wx
import service

class exportHtml():
    
    def refreshFittingHTMl(self):
        settings = service.settings.HTMLExportSettings.getInstance()
        
        if (settings.getEnabled()):
            thread = exportHtmlThread()
            thread.start()

class exportHtmlThread(threading.Thread):
    
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        sMarket = service.Market.getInstance()
        sFit    = service.Fit.getInstance()
        settings = service.settings.HTMLExportSettings.getInstance()

        
        HTML = """
        <!DOCTYPE html> 
        <html> 
            <head> 
            <title>My Page</title> 
            <meta name="viewport" content="width=device-width, initial-scale=1"> 
            <link rel="stylesheet" href="http://code.jquery.com/mobile/1.1.0/jquery.mobile-1.1.0.min.css" />
            <script src="http://code.jquery.com/jquery-1.7.1.min.js"></script>
            <script src="http://code.jquery.com/mobile/1.1.0/jquery.mobile-1.1.0.min.js"></script>
        </head> 
        <body>
        <div data-role="page"> 
        """     
        
        HTML += '<ul data-role="listview" data-inset="true" data-filter="true">';
        categoryList = [];
        self.categoryList = list(sMarket.getShipRoot())
        self.categoryList.sort(key=lambda ship: ship.name)
        for shipType in self.categoryList:
           ships = sMarket.getShipList(shipType.ID)
           for ship in ships:
               HTMLship = '<li><h2>' + ship.name + '</h2><ul>'
               fits = sFit.getFitsWithShip(ship.ID)
               for fit in fits:
                   dnaFit = sFit.exportDna(fit[0])
                   HTMLship += "<li><a href=\"javascript:CCPEVE.showFitting('" + dnaFit + "');\" >" + fit[1] + "</a></li>"

               HTMLship += "</ul></li>"
               if len(fits) > 0:
                   HTML += HTMLship

        HTML += """
        </ul>
        </div>
        </body>"
        """
        
        FILE = open(settings.getPath(), "w")
        FILE.write(HTML);
        FILE.close();
        print "write done"
        
