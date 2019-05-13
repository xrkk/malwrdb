class RefGroup{
    group_id: string;
    update_time: Date;
}

class RefDir{
    _id: string;
    dir_name: string;
}

class RefFile{
    _id: string;
    file_name: string;
    file_size: number;
}

class Sample {
    _id: string;
    sample_name: string;
    smaple_size: number;

    md5: string;
    sha1: string;
    sha128: string;
    sha256: string;
}

class LogLine{
    file: string;
    info: string;
    level: string;
}

class ActiveTask{
    id: string;
    name: string;
    create_time: number;
    start_time: number;
}

class HistoryTask{
    _id: string;
    celery_task_id: string;
    name: string;

    create_time: number;
    start_time: number;
    finish_time: number;
    finish_status: string;
}

export { RefGroup, RefDir, RefFile, Sample, LogLine, ActiveTask, HistoryTask};
