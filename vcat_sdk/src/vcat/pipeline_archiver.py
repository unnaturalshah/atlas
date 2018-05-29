class PipelineArchiver(object):

    def __init__(self, pipeline_name, archive_listing, stage_log_archive, persisted_data_archive, provenance_archive, job_source_archive, artifact_archive, miscellanous_archive):
        self._archive_listing = archive_listing
        self._pipeline_name = pipeline_name
        self._stage_log_archive = stage_log_archive
        self._persisted_data_archive = persisted_data_archive
        self._provenance_archive = provenance_archive
        self._job_source_archive = job_source_archive
        self._artifact_archive = artifact_archive
        self._miscellanous_archive = miscellanous_archive

    def append_stage_log(self, stage_uuid_string, log):
        if log is not None:
            return self._stage_log_archive.append('stage_contexts/' + stage_uuid_string + '/stage_log', log, self._pipeline_name)

    def append_stage_persisted_data(self, stage_uuid_string, data):
        return self.append_persisted_data('stage_persisted/' + stage_uuid_string + '/persisted', data)

    def append_stage_model_data(self, stage_uuid_string, data):
        return self.append_persisted_data('stage_persisted/' + stage_uuid_string + '/model', data)

    def append_persisted_data(self, name, data):
        if data is not None:
            return self._persisted_data_archive.append(name, data, self._pipeline_name)

    def append_provenance(self, provenance):
        if provenance is not None:
            return self._provenance_archive.append('provenance', provenance, self._pipeline_name)

    def append_job_source(self, source_file_path):
        if source_file_path is not None:
            return self._job_source_archive.append_file('job_source', source_file_path, self._pipeline_name)

    def append_artifact(self, name, artifact):
        if artifact is not None:
            return self._artifact_archive.append('artifacts/' + name, artifact, self._pipeline_name)

    def append_miscellanous(self, name, data):
        if data is not None:
            return self._miscellanous_archive.append('miscellaneous/' + name, data, self._pipeline_name)

    def append_tracker(self):
        return self._archive_listing.track_pipeline(self._pipeline_name)

    def fetch_stage_log(self, stage_uuid_string):
        return self._stage_log_archive.fetch('stage_contexts/' + stage_uuid_string + '/stage_log', self._pipeline_name)

    def fetch_stage_persisted_data(self, stage_uuid_string):
        return self.fetch_persisted_data('stage_persisted/' + stage_uuid_string + '/persisted')

    def fetch_stage_model_data(self, stage_uuid_string):
        return self.fetch_persisted_data('stage_persisted/' + stage_uuid_string + '/model')

    def fetch_persisted_data(self, name):
        return self._persisted_data_archive.fetch(name, self._pipeline_name)

    def fetch_provenance(self):
        return self._provenance_archive.fetch('provenance', self._pipeline_name)

    def fetch_job_source(self, target_file_path):
        return self._job_source_archive.fetch_to_file('job_source', target_file_path, self._pipeline_name)

    def fetch_artifact(self, name):
        return self._artifact_archive.fetch('artifacts/' + name, self._pipeline_name)

    def fetch_miscellanous(self, name):
        return self._miscellanous_archive.fetch('miscellaneous/' + name, self._pipeline_name)