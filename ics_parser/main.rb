#!/usr/bin/env ruby

require 'icalendar'
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
    puts "Argument received == #{arguments.first}"
    file_name = arguments.first
    if File.exist? file_name
        puts "FILE EXISTS"

        cal_file = File.open(file_name)
        cals = Icalendar::Calendar.parse(cal_file)

        cal = cals.first

        cal.events.each do |event|
            # pp event
            puts "#####################"
            puts "start date-time: #{event.dtstart}"
            puts "end   date-time: #{event.dtend}"
            puts "start date-time timezone: #{event.dtstart.ical_params['tzid']}"
            puts "summary: #{event.summary}\n\n"
        end
        # event = cal.events.first

        # puts "start date-time: #{event.dtstart}"
        # puts "start date-time timezone: #{event.dtstart.ical_params['tzid']}"
        # puts "summary: #{event.summary}"

        # puts "EVENT SUMMARY == #{event.summary}"

    else
        puts "ERROR: This file doesn't exists"
    end
end
