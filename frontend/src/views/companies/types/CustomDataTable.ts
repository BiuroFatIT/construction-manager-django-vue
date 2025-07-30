export interface Config {
    field: string;
    header: string;
    sortable: boolean;
    filterable: boolean;
    filterType?: 'text' | 'number' | 'date' | 'datetime' | 'select' ;
    filterSelectArray?: Array<any>;
    body?: (row: any) => string;
}

export interface FilterItem {
  value: any;
  matchMode: string;
}
