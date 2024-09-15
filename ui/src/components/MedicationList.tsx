import React, { useState, useEffect } from 'react';
import { Box, Typography } from '@mui/material';
import { DataGrid, GridColDef, GridValueGetterParams } from '@mui/x-data-grid';

interface Medication {
  id: string;
  name: string;
  contents: string;
  objective: string;
  side_effects: string;
  dosage_schedule: string;
}

const columns: GridColDef[] = [
  { field: 'name', headerName: 'Name', flex: 1 },
  { field: 'objective', headerName: 'Objective', flex: 1 },
  { field: 'side_effects', headerName: 'Side Effects', flex: 1 },
  { field: 'dosage_schedule', headerName: 'Dosage', flex: 1 },
  { field: 'contents', headerName: 'Contents', flex: 1 },
];

function MedicationList() {
  const [medications, setMedications] = useState<Medication[]>([]);
  const [page, setPage] = useState(0);
  const [totalRows, setTotalRows] = useState(0);
  const [loading, setLoading] = useState(false);
  const [pageSize, setPageSize] = useState(10);

  useEffect(() => {
    fetchMedications();
  }, [page, pageSize]);

  const fetchMedications = async () => {
    setLoading(true);
    try {
      const response = await fetch(`/api/medications?page=${page + 1}&per_page=${pageSize}`, {
        method: 'GET',
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setMedications(data.medications);
        setTotalRows(data.total_count);
      } else {
        console.error('Failed to fetch medications');
      }
    } catch (error) {
      console.error('Error fetching medications:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ height: 400, width: '100%' }}>
      <Typography variant="h4" gutterBottom>
        Your Medications
      </Typography>
      <DataGrid
        rows={medications}
        columns={columns}
        pagination
        pageSize={pageSize}
        rowsPerPageOptions={[5, 10, 20]}
        rowCount={totalRows}
        paginationMode="server"
        onPageChange={(newPage) => setPage(newPage)}
        onPageSizeChange={(newPageSize) => setPageSize(newPageSize)}
        loading={loading}
        disableSelectionOnClick
      />
    </Box>
  );
}

export default MedicationList;