from collections import defaultdict
import csv
import webbrowser

def readData(heat_file, precip_file, weat_map):
    with open(heat_file, 'r') as heat_file:
        for line in heat_file:
            line = line.split()

            # Reformatting the Dates, without a 0 in a sigle digit we get 
            # unwanted collisions with the temp dates
            if int(line[1]) < 10:   mon = '0' + str(line[1])
            else:   mon = str(line[1])

            if int(line[2]) < 10:   day = '0' + str(line[2])
            else:   day = str(line[2])

            date = str(line[0]) + mon + day # hash-index
            weat_map[date].append(line[0]) # year
            weat_map[date].append(line[1]) # mon
            weat_map[date].append(line[2]) # day
            for i in range(3,5):
                if float(line[i]) < -100: pass # scrubbing bad data
                else:   weat_map[date].append(line[i]) # tmax, tmin

    with open(precip_file, 'r') as precip_file:
        for line in precip_file:
            line = line.split()

            # Reformatting again so our precip dates will collide
            if int(line[1]) < 10:   mon = '0' + str(line[1])
            else:   mon = str(line[1])

            if int(line[2]) < 10:   day = '0' + str(line[2])
            else:   day = str(line[2])

            date = str(line[0]) + mon + day # hash-index
            for i in range(3,6):
                if float(line[i]) < -1: pass # scrubbing bad data
                else:   weat_map[date].append(line[i]) # precip, snow, snowcover

    return weat_map

def writeData(weat_map, writer):
    for k,v in sorted(weat_map.items()):

        # Checking if precip data exists yet
        try:
            row = {'year': weat_map[k][0], 'mon': weat_map[k][1], 'day': weat_map[k][2], 
                   'tmax': weat_map[k][3], 'tmin': weat_map[k][4], 'precip': weat_map[k][5], 
                   'snow': weat_map[k][6], 'snowcover': weat_map[k][7]}
            writer.writerow(row)

        # No precip data yet, only write temp
        except IndexError:
            # It's possible tmax or tmin had bad data
            try:
                writer.writerow({'year': weat_map[k][0], 'mon': weat_map[k][1], 'day': weat_map[k][2], 
                                 'tmax': weat_map[k][3], 'tmin': weat_map[k][4]})
            # No Data possible, pass
            except IndexError:
                pass

def main(weather_file_a, weather_file_b):
    # Declarations
    weather_dict = ['year', 'mon', 'day', 'tmax', 'tmin', 'precip', 'snow', 'snowcover']
    weat_map = defaultdict(list)
    filename = 'weather.csv'

    readData(weather_file_a, weather_file_b, weat_map)

    with open(filename, 'w') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=weather_dict)
        writer.writeheader()
        writeData(weat_map, writer)

    print('CSV created, Generating Graph...')
    execfile("plotlyGenerateGraph.py")
    print('Done. Graph name is WeatherGraph.html')


if __name__ == '__main__':
    main(r'boulder_temperature.txt',
         r'boulder_precipitation.txt')