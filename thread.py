import threading
from opentelemetry import context

from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
)
from opentelemetry import metrics
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (
    ConsoleMetricExporter,
    PeriodicExportingMetricReader,
)

metric_reader = PeriodicExportingMetricReader(ConsoleMetricExporter())
provider = MeterProvider(metric_readers=[metric_reader])

# Sets the global default meter provider
metrics.set_meter_provider(provider)

# Creates a meter from the global meter provider
meter = metrics.get_meter(__name__)
provider = TracerProvider()
processor = BatchSpanProcessor(ConsoleSpanExporter())
provider.add_span_processor(processor)

# Sets the global default tracer provider
trace.set_tracer_provider(provider)

# Creates a tracer from the global tracer provider
tracer = trace.get_tracer(__name__)
 

def print_cube(num, ctx):
    # function to print cube of given num
    context.attach(ctx)
    with tracer.start_as_current_span("child1") as child1:
        current_span.set_attribute("operation.name", "child1!")
        # context.attach(ctx)
        print("Cube: {}" .format(num * num * num))
 
 
def print_square(num, ctx):
    context.attach(ctx)
    with tracer.start_as_current_span("child2") as child1:
        current_span.set_attribute("operation.name", "child1!")
    # function to print square of given num
        print("Square: {}" .format(num * num))
 
 
if __name__ =="__main__":
    # creating thread
    ctx = context.get_current()
    with tracer.start_as_current_span("parent") as parent:
        current_span = trace.get_current_span()
        current_span.set_attribute("operation.name", "Reached parent!")
        
        t1 = threading.Thread(target=print_square, args=(10, ctx))
        t2 = threading.Thread(target=print_cube, args=(10, ctx))

        # with tracer.start_as_current_span("child") as child1:
        #     current_span.set_attribute("operation.name", "child1!")
        #     t1 = threading.Thread(target=print_square, args=(10,))
        # with tracer.start_as_current_span("child") as child2:
        #     current_span.set_attribute("operation.name", "child2!")
        #     t2 = threading.Thread(target=print_cube, args=(10,))
    
        # starting thread 1
        t1.start()
        # starting thread 2
        t2.start()
    
        # wait until thread 1 is completely executed
        t1.join()
        # wait until thread 2 is completely executed
        t2.join()
    
        # both threads completely executed
        print("Done!")