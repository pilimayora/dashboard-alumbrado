require 'mysql2'
require 'active_support/time'

SCHEDULER.every '5m' do
    begin    	
        client = Mysql2::Client.new(:host => "localhost", :username => "root", :password =>"password")
        client.query("USE xys")

        current_time = Time.new
        current_time = current_time.in_time_zone("Europe/Amsterdam")

        points = []

        for i in 1..48
            time_greater_than = current_time - i*60*60 # bottom of timeframe
            time_less_than = time_greater_than + 1*60*60 # top of timeframe

            result = client.query("SELECT * FROM informantes_historico WHERE fecha < '#{time_less_than}' AND fecha > '#{time_greater_than}'")

            numero_informantes = 0

            result.each do |row|
                    numero_informantes = row["informantes_apagados"]
            end

            points << { x: i, y: numero_informantes }
        end

        send_event('informantes_historico', { points: points })

    rescue Exception => e
        puts e.message
    end
end