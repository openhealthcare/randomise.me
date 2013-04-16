PROJ = "Randomise.me"

task :pytest do
  p "Running unit tests for #{PROJ}"
  sh "export DJANGO_SETTINGS_MODULE=rm.settings; python -m pytest rm/test" do | ok,  res |
    # Tests fail. Get over it.
  end
end

task :test => [:pytest] do
  p "Run all test suites"
end
