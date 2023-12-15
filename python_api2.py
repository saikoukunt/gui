import pynwb

class QueryInterface:
    # Class attributes can be defined here if they are constant / shared across all instances
    DATA_STANDARD = "NWB:N"

    def __init__(self, path_to_nwb_file):
        # Instance attributes can be defined here
        self.nwb_path = path_to_nwb_file

    def summarize_nwb_file(self, nwbfile_path):
        """
        Summarizes the contents of an NWB file, printing out the names and the sizes of datasets.

        :param nwbfile_path: Path to the NWB file.
        """
        with pynwb.NWBHDF5IO(nwbfile_path, 'r') as io:
            nwbfile = io.read()
            
            # Print basic file-level metadata
            print("NWB File Summary:")
            print(f"Session ID: {nwbfile.session_id}")
            print(f"Session Description: {nwbfile.session_description}")
            if hasattr(nwbfile, 'identifier'):
                print(f"Identifier: {nwbfile.identifier}")
            if nwbfile.subject:
                print(f"Subject ID: {nwbfile.subject.subject_id}")
            print("\n")

            # Summarize processing modules
            if nwbfile.processing:
                print("Processing Modules:")
                for module_name, module in nwbfile.processing.items():
                    print(f"- {module_name}: {len(module.data_interfaces)} interfaces")

            # Summarize acquisitions
            print("Acquisitions:")
            for acq_name, acq_data in nwbfile.acquisition.items():
                if hasattr(acq_data, 'data') and hasattr(acq_data.data, 'shape'):
                    data_shape = acq_data.data.shape
                else:
                    data_shape = 'N/A'
                print(f"- {acq_name}: Shape = {data_shape}")

            # Summarize units, if they exist
            if hasattr(nwbfile, 'units') and nwbfile.units is not None:
                print("Units:")
                print(f"- Units: Count = {len(nwbfile.units.id.data)}")

            # Add other specific groups you are interested in

# Example usage:
# summarize_nwb_file('path_to_your_file.nwb')

    def explore_nwb_file(self, nwbfile_path):
        """
        Explores the contents of an NWB file and prints out the metadata and structure.

        :param nwbfile_path: Path to the NWB file.
        """
        with pynwb.NWBHDF5IO(nwbfile_path, 'r') as io:
            nwbfile = io.read()
            print("Metadata:")
            print(f"Session ID: {nwbfile.session_id}")
            print(f"Experiment description: {nwbfile.experiment_description}")
            print(f"Subject: {nwbfile.subject}")
            print("\n")

            print("Data Structure:")
            # Iterate through all processing modules
            if nwbfile.processing:
                for module_name, module in nwbfile.processing.items():
                    print(f"Processing Module: {module_name}")
                    for interface_name, data_interface in module.data_interfaces.items():
                        print(f"  Data Interface: {interface_name}")
                        print(f"    Type: {type(data_interface)}")
                        # Add more specific print statements based on the type of data_interface
                        # For example, if data_interface is an ImageSeries, print some image data properties

            # Iterate through all acquisition data
            print("Acquisitions:")
            for acq_name, acq_data in nwbfile.acquisition.items():
                print(f"  Acquisition: {acq_name}")
                print(f"    Type: {type(acq_data)}")
                # Similarly, add more specific print statements based on the type of acq_data

            # Print units if they exist (typically contains spike times)
            if nwbfile.units is not None:
                print("Units:")
                for unit_id in nwbfile.units.id.data:
                    print(f"  Unit ID: {unit_id}")
                    for col in nwbfile.units.colnames:
                        print(f"    {col}: {nwbfile.units[col][unit_id]}")

            # Add other specific groups you are interested in

    # Example usage:
    # explore_nwb_file('path_to_your_file.nwb')


    def retrieve_spike_times(self, nwbfile_path):
        """
        Retrieves spike times for each unit ID from an NWB file and stores them in a dictionary.

        :param nwbfile_path: Path to the NWB file.
        :return: Dictionary with unit IDs as keys and spike times as values.
        """
        spike_times_per_unit = {}

        with pynwb.NWBHDF5IO(nwbfile_path, 'r') as io:
            nwbfile = io.read()

            # Ensure that the units table exists
            if hasattr(nwbfile, 'units') and nwbfile.units is not None:
                # Loop through each unit
                for unit_id in nwbfile.units.id.data[:]:
                    # Retrieve the spike times for the current unit
                    unit_spike_times = nwbfile.units['spike_times'][unit_id]

                    # Store the spike times in the dictionaryc
                    spike_times_per_unit[unit_id] = unit_spike_times[:]

        return spike_times_per_unit

    # Example usage:
    # spike_times_dict = retrieve_spike_times('path_to_your_file.nwb')
    # print(spike_times_dict)


    def query_data(self, file_path, query_parameters):
        """
        Query subsets of data based on metadata.
        :param file_path: Path to the NWB file.
        :param query_parameters: Dictionary of parameters for querying the data.
        :return: The subset of the data that matches the query.
        """
        # Implementation for querying data
        pass

    def lazy_load_data(self, nwbfile_path, unit_id, chunk_size=100):
            """
            Lazily loads spike times data for a specified unit ID from an NWB file.

            :param nwbfile_path: Path to the NWB file.
            :param unit_id: The ID of the unit whose spike times are to be loaded.
            :param chunk_size: The number of spike times to read at a time.
            :yield: A chunk of spike times until all spike times are yielded.
            """
            with pynwb.NWBHDF5IO(nwbfile_path, 'r') as io:
                nwbfile = io.read()

                # Check if units and the specified unit exist
                if hasattr(nwbfile, 'units') and unit_id in nwbfile.units.id.data[:]:
                    # Determine the index of the unit ID
                    unit_index = list(nwbfile.units.id.data[:]).index(unit_id)
                    
                    # Determine the total number of spikes
                    total_spikes = len(nwbfile.units['spike_times'][unit_index])

                    # Yield chunks of spike times
                    for start_idx in range(0, total_spikes, chunk_size):
                        end_idx = min(start_idx + chunk_size, total_spikes)
                        # Fetch the chunk of spike times
                        spike_times_chunk = nwbfile.units['spike_times'][unit_index][start_idx:end_idx]
                        yield spike_times_chunk

    # Data Manipulations Functions
    def update_data(self, file_path, data):
        """
        Update an NWB file with new data.
        :param file_path: Path to the NWB file.
        :param data: New data to write into the file.
        """
        # Implementation for updating data in an NWB file
        pass

    def retrieve_spike_times(self, nwbfile_path):
        """
        Retrieves spike times for each unit ID from an NWB file and stores them in a dictionary.

        :param nwbfile_path: Path to the NWB file.
        :return: Dictionary with unit IDs as keys and spike times as values.
        """
        spike_times_per_unit = {}

        with pynwb.NWBHDF5IO(nwbfile_path, 'r') as io:
            nwbfile = io.read()

            # Ensure that the units table exists
            if hasattr(nwbfile, 'units') and nwbfile.units is not None:
                # Loop through each unit
                for unit_id in nwbfile.units.id.data[:]:
                    # Retrieve the spike times for the current unit
                    unit_spike_times = nwbfile.units['spike_times'][unit_id]

                    # Store the spike times in the dictionary
                    spike_times_per_unit[unit_id] = unit_spike_times[:]

        return spike_times_per_unit

    def write_data(self, file_path, data):
        """
        Write data to an NWB file.
        :param file_path: Path to the NWB file.
        :param data: Data to write into the file.
        """
        # Implementation for writing data to an NWB file
        pass

    # Integration Functions for Extensions
    def convert_data(self, data, to_format):
        """
        Convert data between NWB format and another format.
        :param data: Data to convert.
        :param to_format: The format to convert the data to.
        :return: The converted data.
        """
        # Implementation for data conversion
        pass


# Test case
example_path = 'sub-P9HMH_ses-20060301_obj-1otd1m8_ecephys+image.nwb'
query_interface = QueryInterface(example_path)
# query_interface.explore_nwb_file(query_interface.nwb_path)
query_interface.summarize_nwb_file(query_interface.nwb_path)
# retrieve_spike_times = query_interface.retrieve_spike_times(query_interface.nwb_path)
# print(retrieve_spike_times)