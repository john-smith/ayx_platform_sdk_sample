import React, { useContext, useEffect} from 'react';
import ReactDOM from 'react-dom';
import { AyxAppWrapper, Box, Grid, Typography, makeStyles, Theme, TextField } from '@alteryx/ui';
import { Alteryx } from '@alteryx/icons';
import { Context as UiSdkContext, DesignerApi } from '@alteryx/react-comms';



const useStyles = makeStyles((theme: Theme) => ({
  alteryx: {
    color: theme.palette.brand.corporateBlue,
    height: '125px',
    width: '125px'
  }
}));

const App = () => {
  const classes = useStyles();
  const [model, handleUpdateModel] = useContext(UiSdkContext);


  // Dev Harness Specific Code ---------- Start
  // The following code is specifically a dev harness functionality.
  // If you're developing a tool for Designer, you'll want to remove this
  // and check out our docs for guidance 
  useEffect(() => {
    handleUpdateModel(model)
  }, []);
  // Dev Harness Specific Code ---------- End

  const new_column = event => {
    const newModel = { ...model };
    newModel.Configuration.new_column = event.target.value;
    handleUpdateModel(newModel);
  }
  

  return (
    <Box p={4}>
     <Grid container spacing={4} direction="column" alignItems="center">
        <Grid item>
          <TextField id="new_column" 
            onChange={new_column} 
            value={model.Configuration.new_column} 
            label="データを入力" /> 
        </Grid>
        <Grid item>
        </Grid>
      </Grid>
    </Box>
  )
}

const Tool = () => {
  return (
    <DesignerApi messages={{}} defaultConfig={{ 
      Configuration: { 
        new_column : ""
      }
    }}>
      <AyxAppWrapper> 
        <App />
      </AyxAppWrapper>
    </DesignerApi>
  )
}

ReactDOM.render(
  <Tool />,
  document.getElementById('app')
);
