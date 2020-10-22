import cups


cups.setUser("PRATIK")

conn = cups.Connection()

printers = conn.getPrinters()
printer_keys = list(printers.items())
deviceuri = printer_keys[1][1]['device-uri']


#print(dir(printers))

# print(conn.getS(printer_keys[0]))
print(conn.getJobs(which_jobs='all', my_jobs=False))
# print(conn.getPrinterAttributes(printername, requested_attributes=["pages-per-minute"]))
# for print(printers)printer in printers:
#     print(printer, printers[printer]["device-uri"],'\n')
