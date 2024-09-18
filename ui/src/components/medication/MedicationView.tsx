import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { Card, CardContent, Typography, CircularProgress, Box } from '@mui/material';

interface Medication {
  id: string;
  name: string;
  contents: string;
  objective: string;
  side_effects: string;
  dosage_schedule: string;
}

const MedicationView: React.FC = () => {
  const [medication, setMedication] = useState<Medication | null>(null);
  const [loading, setLoading] = useState(true);
  const { id } = useParams<{ id: string }>();

  useEffect(() => {
    const fetchMedication = async () => {
      try {
        const response = await fetch(`/api/medications/medication/${id}`, {
          method: 'GET',
          credentials: 'include',
        });
        if (response.ok) {
          const data = await response.json();
          setMedication(data);
        } else {
          console.error('Failed to fetch medication');
        }
      } catch (error) {
        console.error('Error fetching medication:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchMedication();
  }, [id]);

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" height="100vh">
        <CircularProgress />
      </Box>
    );
  }

  if (!medication) {
    return <Typography>Medication not found</Typography>;
  }

  return (
    <Card>
      <CardContent>
        <Typography variant="h5" component="div" gutterBottom>
          {medication.name}
        </Typography>
        <Typography variant="body1" paragraph>
          <strong>Objective:</strong> {medication.objective}
        </Typography>
        <Typography variant="body1">
          <strong>Dosage Schedule:</strong> {medication.dosage_schedule}
        </Typography>
        <Typography variant="body1" paragraph>
          <strong>Side Effects:</strong> {medication.side_effects}
        </Typography>
        <Typography variant="body1" paragraph>
          <strong>Contents:</strong> {medication.contents}
        </Typography>
      </CardContent>
    </Card>
  );
};

export default MedicationView;