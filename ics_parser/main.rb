#!/usr/bin/env ruby
# coding: utf-8

require 'icalendar'
require 'json'
require_relative 'server.rb'

arguments = ARGV

if arguments.first.nil?
    port = 2000

    server = Server.new(port)
    puts "ICS PARSER STARTED"

    server.listen do |client|
        puts "ICS PARSER LISTENING"
        file_name = client.gets.chomp
        if File.exist? file_name
            client.puts "FILE EXISTS"

            cal_file = File.open(file_name)
            cals = Icalendar::Calendar.parse(cal_file)

            cal = cals.first
            event = cal.events.first

            puts "start date-time: #{event.dtstart}"
            puts "start date-time timezone: #{event.dtstart.ical_params['tzid']}"
            puts "summary: #{event.summary}"

            client.puts "EVENT SUMMARY == #{event.summary}"

        else
            client.puts "ERROR: Invalid filename"
        end
    end
elsif arguments.first == "help"
    puts "Usage: ./ics_parser path/to/file.ics"
else
    file_name = arguments.first
    if File.exist? file_name
        cal_file = File.open(file_name)
        cals = Icalendar::Calendar.parse(cal_file)

        cal = cals.first

        position = 0
        events = []

        cal.events.each do |event|
            # Se o evento tiver um horário específico para acontecer
            if event.dtstart.is_a?(Icalendar::Values::DateTime)
                events[position] = {
                    start: {
                        year:   event.dtstart.year,
                        month:  event.dtstart.month,
                        day:    event.dtstart.day,
                        hour:   event.dtstart.hour,
                        minute: event.dtstart.min,
                        second: event.dtstart.sec
                    },
                    end: {
                        year:   event.dtend.year,
                        month:  event.dtend.month,
                        day:    event.dtend.day,
                        hour:   event.dtend.hour,
                        minute: event.dtend.min,
                        second: event.dtend.sec
                    },
                    timezone: event.dtstart.ical_params['tzid'],
                    summary: event.summary.to_s
                }
                position += 1
            end
        end

        puts events.to_json

    else
        puts ({ERROR: "File doesn't exists"}).to_json
    end
end
