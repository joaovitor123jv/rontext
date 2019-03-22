    require 'socket'

APPLICATION_KEY = "CTXTSEARCH"

class Server
    def initialize(port)
        @port = port
        @server = TCPServer.open(port)
    end

    def listen
        loop do
            Thread.start(@server.accept) do |client|
                puts "CLIENTE ACEITO"
                if client.gets.chomp == APPLICATION_KEY
                    puts "CHAVE CORRETA"
                    yield(client)
                else
                    client.puts "ERROR, WRONG KEY"
                    client.close
                end
            end
        end
    end
end