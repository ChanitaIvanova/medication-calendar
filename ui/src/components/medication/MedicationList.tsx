import React, { useState, useEffect } from 'react';
import { Box, Typography, Paper, Button } from '@mui/material';
import { DataGrid, GridColDef, GridSortModel, GridFilterModel, GridFilterInputValue, GridRowSelectionModel } from '@mui/x-data-grid';
import { useTheme, useMediaQuery } from '@mui/material';
import { Dialog, DialogActions, DialogContent, DialogContentText, DialogTitle } from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import EditIcon from '@mui/icons-material/Edit';
import VisibilityIcon from '@mui/icons-material/Visibility';
import { useNavigate } from 'react-router-dom';
import { medicationService } from '../../services/medicationService';

interface Medication {
  id: string;
  name: string;
  contents: string;
  objective: string;
  side_effects: string;
  dosage_schedule: string;
}

const getCommonFilterOperators = () => [
  {
    label: 'contains',
    value: 'contains',
    getApplyFilterFn: (filterItem) => {
      return (params) => {
        return params.value.toLowerCase().includes(filterItem.value.toLowerCase());
      };
    },
    InputComponent: GridFilterInputValue,
  },
];

const commonColumnProperties = {
  flex: 2,
  minWidth: 250,
  filterable: true,
  renderCell: (params) => (
    <div style={{ 
      whiteSpace: 'pre-wrap', 
      wordBreak: 'break-word',
      overflowWrap: 'break-word',
      padding: '8px',
      width: '100%',
      height: '100%',
      overflow: 'auto'
    }}>
      {params.value}
    </div>
  ),
  filterOperators: getCommonFilterOperators(),
};

const columns: GridColDef[] = [
  { 
    field: 'name', 
    headerName: 'Name', 
    flex: 1, 
    minWidth: 150, 
    filterable: true,
    filterOperators: getCommonFilterOperators(),
  },
  { 
    field: 'objective', 
    headerName: 'Objective', 
    display: "flex",
    ...commonColumnProperties,
  },
  { 
    field: 'dosage_schedule', 
    headerName: 'Dosage', 
    ...commonColumnProperties,
  },
  { 
    field: 'side_effects', 
    headerName: 'Side Effects', 
    ...commonColumnProperties,
    hideable: true,
    hide: true,
  },
  { 
    field: 'contents', 
    headerName: 'Contents', 
    ...commonColumnProperties,
    hideable: true,
    hide: true,
  },
];

function MedicationList() {
  const [medications, setMedications] = useState<Medication[]>([]);
  const [page, setPage] = useState(0);
  const [totalRows, setTotalRows] = useState(0);
  const [loading, setLoading] = useState(false);
  const [pageSize, setPageSize] = useState(10);
  const [sortModel, setSortModel] = useState<GridSortModel>([]);
  const [filterModel, setFilterModel] = useState<GridFilterModel>({
    items: [],
  });
  const [selectedMedication, setSelectedMedication] = useState<string | null>(null);
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [rowSelectionModel, setRowSelectionModel] = useState<GridRowSelectionModel>([]);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const navigate = useNavigate();

  useEffect(() => {
    fetchMedications();
  }, [page, pageSize, sortModel, filterModel]);

  const fetchMedications = async () => {
    setLoading(true);
    try {
      const sortField = sortModel.length > 0 ? sortModel[0].field : '';
      const sortDirection = sortModel.length > 0 ? sortModel[0].sort : '';
      
      const filterParams = filterModel.items.reduce((acc, filter) => {
        if (filter.value) {
          acc[filter.field] = filter.value;
        }
        return acc;
      }, {} as Record<string, string>);

      const params = {
        page: page + 1,
        per_page: pageSize,
        sort_field: sortField,
        sort_direction: sortDirection || '',
        ...filterParams
      };

      const data = await medicationService.fetchMedications(params);
      setMedications(data.medications);
      setTotalRows(data.total_count);
    } catch (error) {
      console.error('Error fetching medications:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async () => {
    if (selectedMedication) {
      try {
        await medicationService.deleteMedication(selectedMedication);
        fetchMedications();
        setDeleteDialogOpen(false);
        setSelectedMedication(null);
        setRowSelectionModel([]);
      } catch (error) {
        console.error('Error deleting medication:', error);
      }
    }
  };

  const getVisibleColumns = () => {
    if (isMobile) {
      return columns.filter(col => col.field === 'name');
    }
    return columns;
  };

  return (
    <Box sx={{ height: '100%', width: '100%', display: 'flex', flexDirection: 'column' }}>
      <Typography variant="h4" gutterBottom>
        Your Medications
      </Typography>
      <Box sx={{ mb: 2 }}>
        <Button
          startIcon={<VisibilityIcon />}
          disabled={!selectedMedication}
          onClick={() => navigate(`/medications/${selectedMedication}`)}
        >
          View
        </Button>
        <Button
          startIcon={<EditIcon />}
          disabled={!selectedMedication}
          onClick={() => navigate(`/edit-medication/${selectedMedication}`)}
        >
          Edit
        </Button>
        <Button
          startIcon={<DeleteIcon />}
          disabled={!selectedMedication}
          onClick={() => setDeleteDialogOpen(true)}
        >
          Delete
        </Button>
      </Box>
      <Paper sx={{ flexGrow: 1, width: '100%', height: "100%", overflow: 'hidden' }}>
        <DataGrid
          autoHeight
          rows={medications}
          columns={getVisibleColumns()}
          pagination
          paginationMode="server"
          rowCount={totalRows}
          pageSize={pageSize}
          rowsPerPageOptions={isMobile ? [5, 10] : [5, 10, 20]}
          onPageChange={(newPage) => setPage(newPage)}
          onPageSizeChange={(newPageSize) => setPageSize(newPageSize)}
          sortingMode="server"
          onSortModelChange={(newSortModel) => setSortModel(newSortModel)}
          filterMode="server"
          onFilterModelChange={(newFilterModel) => setFilterModel(newFilterModel)}
          loading={loading}
          checkboxSelection={false}
          onRowSelectionModelChange={(newRowSelectionModel) => {
            setRowSelectionModel(newRowSelectionModel);
            setSelectedMedication(newRowSelectionModel[0] as string | null);
          }}
          rowSelectionModel={rowSelectionModel}
          getRowHeight={() => 'auto'}
          getEstimatedRowHeight={() => 200}
          initialState={{
            columns: {
              columnVisibilityModel: {
                contents: false,
              },
            },
          }}
          sx={{
            '& .MuiDataGrid-cell': {
              padding: isMobile ? '8px 4px' : '8px 16px',
            },
            '& .MuiDataGrid-columnHeader': {
              padding: isMobile ? '8px 4px' : '8px 16px',
            },
          }}
        />
      </Paper>
      <Dialog
        open={deleteDialogOpen}
        onClose={() => setDeleteDialogOpen(false)}
      >
        <DialogTitle>Confirm Delete</DialogTitle>
        <DialogContent>
          <DialogContentText>
            Are you sure you want to delete this medication?
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleDelete} color="error">Delete</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
}

export default MedicationList;